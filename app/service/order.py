from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model.member import Member
from app.model.order import Order
from app.schema.order import OrderCreate

class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate, member_id: int):
        # 사용자 정보 조회
        member = db.query(Member).filter(Member.mno == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        # 주문 생성
        new_order = Order(
            mno=member.mno,
            prdno=order.prdno,
            qty=order.qty,
            price=order.price,
            postcode=member.postcode,
            addr=member.address,
            phone=member.phone,
            regdate=datetime.now()
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    @staticmethod
    def get_order(db: Session, omno: int):
        db_order = db.query(Order).filter(Order.omno == omno).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order

    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Order).offset(skip).limit(limit).all()

