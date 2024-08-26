from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    mno: int
    prdno: int
    size: str
    qty: int
    price: int
    postcode: str
    addr: str
    phone: str

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    omno: int
    regdate: Optional[datetime]

