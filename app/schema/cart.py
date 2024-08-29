from pydantic import BaseModel

class CartBase(BaseModel):
    mno: int
    prdno: int
    qty: int
    price: int

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass

class CartInDBBase(CartBase):
    cno: int  # Cart ID

    class Config:
        from_attributes = True

class Cart(CartInDBBase):
    pass

class CartInDB(CartInDBBase):
    pass
