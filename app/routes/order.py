from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.order import Order
from app.schema.order import OrderCreate, OrderRead
from app.dbfactory import get_db

order_router = APIRouter()

# order 라우터 주문번호에 따른 엔드포인트 지정
# 관리자입장 / 회원입장 라우트 된 엔트포인트가 달라야 한다

# ex)
# member/order/{prdno}
# admin/order/{prdno}

@order_router.post("/order/", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@order_router.get("/order/{omno}", response_model=OrderRead)
def read_order(omno: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.omno == omno).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
