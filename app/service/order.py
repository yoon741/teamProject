from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.order import Order
from app.schema.order import OrderCreate

def create_order(db: Session, order: OrderCreate):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_order(db: Session, omno: int):
    db_order = db.query(Order).filter(Order.omno == omno).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()
