from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Outlet(BaseModel):
    outlet_id: int
    outlet_name: str
    location: str
    contact_info: Optional[str] = None

class Customer(BaseModel):
    customer_id: int
    name: str
    phone_number: Optional[str]
    email: Optional[str]
    created_at: datetime

class OrderItem(BaseModel):
    item_id: int
    order_id: str
    item_name: str
    quantity: int
    price_per_unit: float
    total_price: float

class Order(BaseModel):
    order_id: str
    outlet_id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    payment_mode: str
    status: str
    items: List[OrderItem]

class WebhookPayload(BaseModel):
    customer: Customer
    outlet: Outlet
    order: Order
