from typing import Optional

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., examples=["Laptop"])
    description: Optional[str] = Field(None, examples=["16GB RAM, 512GB SSD"])
    price: float = Field(..., gt=0, examples=[999.99])


class ItemResponse(ItemCreate):
    id: str
