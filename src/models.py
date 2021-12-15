"""
models.py
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class DeliveryIn(BaseModel):
    product_id: int
    count: int
    country: Optional[str] = "RU"


class DeliveryMethod(BaseModel):
    service: str
    value: float
    currency: str
    date: Optional[date]


class DeliveryOut(BaseModel):
    delivery: List[DeliveryMethod]


class ProductIn(BaseModel):
    product_id: int
    sku_id: Optional[int] = None


class ProductSKU(BaseModel):
    sku_url: str
    sku_id: int
    quantity: int
    price: float


class ProductOut(BaseModel):
    name: str
    description: str
    likes: int
    rating: float
    reviews: int
    store_url: str
    seller_id: int
    sku: List[ProductSKU]
