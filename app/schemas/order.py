from pydantic import BaseModel
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id:int
    quantity:int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id:int
    price:float


class OrderBase(BaseModel):
    pass 


class OrderCreate(OrderBase):
    items:list[OrderItemCreate]


class Order(OrderBase):
    id:int
    user_id:int
    created_at:datetime
    status:str
    total_price:float
    items:list[OrderItem]