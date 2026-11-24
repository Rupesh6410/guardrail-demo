from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200)
    item: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=1, le=1000)
    price: float = Field(..., ge=0)


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_name: str
    item: str
    quantity: int
    price: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
