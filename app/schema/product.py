from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class ProductBase(BaseModel):
    prdname: str
    price: str
    size: str
    color: str
    material: str
    brand: str
    style: str
    weight: str
    origin: str
    description: str

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    prdno: int
    regdate: datetime

    class Config:
        from_attributes = True

class PrdAttachBase(BaseModel):
    prdno: int
    img1: str
    img2: str
    img3: str
    img4: str

class PrdAttachCreate(PrdAttachBase):
    pass

class PrdAttachRead(PrdAttachBase):
    prdatno: int
