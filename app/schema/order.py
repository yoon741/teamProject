from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    mno: int
    prdno: int
    qty: int
    price: int
    postcode: str
    addr: str
    phone: str
    payment: str

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    omno: int  # 주문 번호
    regdate: Optional[datetime]

    class Config:
        from_attributes = True  # ORM 호환 모드
