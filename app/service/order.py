from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.order import Order as OrderModel
from app.model.member import Member
from app.model.product import Product
from app.service.cart import CartService

class OrderService:

    @staticmethod
    def get_member_by_mno(db: Session, mno: int):
        member = db.query(Member).filter(Member.mno == mno).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")
        return member

    @staticmethod
    def get_product_by_prdno(db: Session, prdno: int):
        product = db.query(Product).filter(Product.prdno == prdno).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def create_order(
            db: Session,
            mno: int,
            prdno: int,
            qty: int,
            price: int,
            postcode: str,
            addr: str,
            phone: str,
            payment: str
    ) -> OrderModel:
        try:
            # 회원 정보 조회
            member = db.query(Member).filter(Member.mno == mno).first()
            if not member:
                raise HTTPException(status_code=404, detail="User not found")

            # 제품 정보 조회
            product = db.query(Product).filter(Product.prdno == prdno).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            # 새로운 주문 번호 생성
            order_number = db.query(func.max(OrderModel.omno)).scalar() + 1 if db.query(func.count(OrderModel.omno)).scalar() > 0 else 1

            # 새로운 주문 생성
            new_order = OrderModel(
                omno=order_number,
                mno=mno,
                prdno=prdno,
                qty=qty,
                price=price,
                postcode=postcode,
                addr=addr,
                phone=phone,
                payment=payment
            )

            # 주문 저장
            db.add(new_order)
            db.refresh()
            db.commit()
            db.refresh(new_order)

            # 장바구니 아이템 제거
            CartService.clear_cart_items(db, member.userid)

            return new_order

        except Exception as ex:
            db.rollback()
            print(f'Create Order Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to create order")

    @staticmethod
    def get_order(db: Session, omno: int):
        try:
            order = db.query(OrderModel).filter(OrderModel.omno == omno).first()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return order

        except Exception as ex:
            print(f'Get Order Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to retrieve order")

    @staticmethod
    def get_orders_by_userid(db: Session, userid: str):
        try:
            member = db.query(Member).filter(Member.userid == userid).first()
            if not member:
                raise HTTPException(status_code=404, detail="User not found")

            orders = db.query(OrderModel).filter(OrderModel.mno == member.mno).all()
            return orders

        except Exception as ex:
            print(f'Get Orders By UserID Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to retrieve orders")

    @staticmethod
    def process_cart_order(db: Session, userid: str, addr: str, phone: str, postcode: str):
        try:
            member = db.query(Member).filter(Member.userid == userid).first()
            if not member:
                raise HTTPException(status_code=404, detail="User not found")

            cart_items = CartService.get_cart_items_by_userid(db, userid)
            if not cart_items:
                raise HTTPException(status_code=404, detail="No items in cart")

            order_number = db.query(func.max(OrderModel.omno)).scalar() + 1 if db.query(func.count(OrderModel.omno)).scalar() > 0 else 1

            for item in cart_items:
                new_order = OrderModel(
                    omno=order_number,
                    mno=member.mno,
                    prdno=item.prdno,
                    qty=item.qty,
                    price=item.price,
                    addr=addr,
                    phone=phone,
                    postcode=postcode
                )
                db.add(new_order)

            db.commit()

            CartService.clear_cart_items(db, userid)

            return True

        except Exception as ex:
            db.rollback()
            print(f'Process Cart Order Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to process cart order")

    @staticmethod
    def get_member_info(db: Session, userid: str):
        try:
            member = db.query(Member).filter(Member.userid == userid).first()
            if not member:
                raise HTTPException(status_code=404, detail="User not found")
            return member

        except Exception as ex:
            print(f'Get Member Info Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to retrieve member info")
