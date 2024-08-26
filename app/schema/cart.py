from pydantic import BaseModel

class CartBase(BaseModel):
    mno: int
    prdno: int
    size: str
    qty: int
    price: int

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    cno: int

