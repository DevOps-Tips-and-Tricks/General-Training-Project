import json
import uuid
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from redis import Redis

from app.database import get_redis
from app.schemas import ItemCreate, ItemResponse

# Create a router instance for items
router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, redis_client: Redis = Depends(get_redis)):
    item_id = str(uuid.uuid4())
    item_dict = item.model_dump()
    item_dict["id"] = item_id

    redis_client.set(f"item:{item_id}", json.dumps(item_dict))
    return item_dict


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: str, redis_client: Redis = Depends(get_redis)):
    item_data = redis_client.get(f"item:{item_id}")
    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found")

    return json.loads(item_data)


@router.get("/", response_model=List[ItemResponse])
def list_items(redis_client: Redis = Depends(get_redis)):
    keys = redis_client.keys("item:*")
    items = []
    for key in keys:
        item_data = redis_client.get(key)
        if item_data:
            items.append(json.loads(item_data))

    return items


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str, item: ItemCreate, redis_client: Redis = Depends(get_redis)
):
    if not redis_client.exists(f"item:{item_id}"):
        raise HTTPException(status_code=404, detail="Item not found")

    item_dict = item.model_dump()
    item_dict["id"] = item_id

    redis_client.set(f"item:{item_id}", json.dumps(item_dict))
    return item_dict


@router.delete("/{item_id}")
def delete_item(item_id: str, redis_client: Redis = Depends(get_redis)):
    result = redis_client.delete(f"item:{item_id}")
    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}
