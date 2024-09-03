from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ProductBase 모델
class ProductBase(BaseModel):
    prdname: str
    price: str
    type: str
    qty: int

# ProductCreate 모델: 생성 시 사용
class ProductCreate(ProductBase):
    pass

# ProductRead 모델: 조회 시 사용
class ProductRead(ProductBase):
    prdno: int
    regdate: datetime

    class Config:
        from_attributes = True

# PrdAttachBase 모델
class PrdAttachBase(BaseModel):
    prdno: int
    img1: str
    img2: str
    img3: str
    img4: str

# PrdAttachCreate 모델: 생성 시 사용
class PrdAttachCreate(PrdAttachBase):
    pass

# PrdAttachRead 모델: 조회 시 사용
class PrdAttachRead(PrdAttachBase):
    prdatno: int


class NewProduct(BaseModel):
    prdname: str
    price: int
    type: str
    qty: int
    description: str