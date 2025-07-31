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

class Tax(BaseModel):
    tax_name: str
    tax_rate: float
    tax_amount: float

class Discount(BaseModel):
    discount_type: str
    discount_value: float
    discount_reason: Optional[str] = None

class Order(BaseModel):
    order_id: str
    outlet_id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    payment_mode: str
    status: str
    order_type: Optional[str] = None
    payment_type: Optional[str] = None
    created_on: Optional[datetime] = None
    order_from: Optional[str] = None
    items: List[OrderItem]
    taxes: Optional[List[Tax]] = []
    discounts: Optional[List[Discount]] = []


class WebhookPayload(BaseModel):
    customer: Customer
    outlet: Outlet
    order: Order