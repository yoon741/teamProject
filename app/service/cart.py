import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.product import Cart as CartModel
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
            cart_item = CartService.get_cart_item_by_cno(db, cno)

            db.delete(cart_item)
            db.commit()
            return cart_item
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete cart item: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete cart item")
