from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.cart import Cart
from app.schema.cart import CartCreate

def create_cart_item(db: Session, cart: CartCreate):
    new_cart = Cart(**cart.dict())
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

def get_cart_item(db: Session, cno: int):
    db_cart = db.query(Cart).filter(Cart.cno == cno).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return db_cart

def get_cart_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cart).offset(skip).limit(limit).all()
