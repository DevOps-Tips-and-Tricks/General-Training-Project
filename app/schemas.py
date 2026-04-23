from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str = Field(..., example="Laptop")
    description: Optional[str] = Field(None, example="16GB RAM, 512GB SSD")
    price: float = Field(..., gt=0, example=999.99)


class ItemResponse(ItemCreate):
    id: str
