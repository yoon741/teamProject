import logging
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.model.member import Member
from app.model.product import Cart as CartModel
from app.model.product import Product as ProductModel
from app.schema.cart import CartCreate, CartUpdate

logger = logging.getLogger(__name__)

class CartService:
    @staticmethod
    def create_cart_item(db: Session, cart: CartCreate):
        try:
            cart_item = CartModel(**cart.dict())
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)  # 새로운 객체의 상태를 데이터베이스와 동기화
            return cart_item
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create cart item: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create cart item")

    @staticmethod
    def get_cart_item_by_cno(db: Session, cno: int):
        try:
            cart_item = db.query(CartModel).filter(CartModel.cno == cno).first()
            if not cart_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
            return cart_item
        except Exception as e:
            logger.error(f"Failed to retrieve cart item: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve cart item")

    @staticmethod
    def update_cart_item(db: Session, cno: int, cart_update: CartUpdate):
        try:
            cart_item = CartService.get_cart_item_by_cno(db, cno)
            for key, value in cart_update.dict(exclude_unset=True).items():
                setattr(cart_item, key, value)
            db.commit()
            db.refresh(cart_item)
            return cart_item
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update cart item: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update cart item")

    @staticmethod
    def delete_cart_item(db: Session, cno: int):
        try:
            logger.info(f"Trying to delete cart item with cno: {cno}")

            cart_item = CartService.get_cart_item_by_cno(db, cno)

            if not cart_item:
                logger.error(f"No cart item found with cno: {cno}")
                raise HTTPException(status_code=404, detail="Cart item not found")

            db.delete(cart_item)
            db.commit()

            logger.info(f"Cart item with cno: {cno} deleted successfully")
            return {"message": "Cart item deleted successfully"}
        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()  # 오류 발생 시 롤백
            logger.error(f"Failed to delete cart item: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete cart item")


    @staticmethod
    def get_cart_items_by_userid(db: Session, userid: str):
        member = db.query(Member).filter(Member.userid == userid).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")
        cart_items = db.query(CartModel).options(joinedload(CartModel.product)).filter(CartModel.mno == member.mno).all()
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items in cart")
        return cart_items

    @staticmethod
    def add_to_cart(db: Session, userid: str, prdno: int, qty: int):
        member = db.query(Member).filter(Member.userid == userid).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")
        product = db.query(ProductModel).filter_by(prdno=prdno).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.qty < qty:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        cart_item = db.query(CartModel).filter(CartModel.mno == member.mno, CartModel.prdno == prdno).first()
        if cart_item:
            cart_item.qty += qty
            cart_item.price = cart_item.qty * product.price
        else:
            cart_item = CartModel(mno=member.mno, prdno=prdno, qty=qty, price=qty * product.price)
            db.add(cart_item)
        product.qty -= qty
        db.commit()

    @staticmethod
    def clear_cart_items(db: Session, userid: str):
        member = db.query(Member).filter(Member.userid == userid).first()
        if not member:
            raise HTTPException(status_code=404, detail="User not found")
        db.query(CartModel).filter(CartModel.mno == member.mno).delete()
        db.commit()
