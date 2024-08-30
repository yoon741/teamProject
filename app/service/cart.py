from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.product import Cart as CartModel
from app.schema.cart import CartCreate, CartUpdate

class CartService:
    @staticmethod
    def create_cart_item(db: Session, cart: CartCreate):
        db_cart = CartModel(**cart.dict())
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart

    @staticmethod
    def get_cart_item(db: Session, cno: int):
        db_cart = db.query(CartModel).filter(CartModel.cno == cno).first()
        if db_cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return db_cart

    @staticmethod
    def update_cart_item(db: Session, cno: int, cart: CartUpdate):
        db_cart = db.query(CartModel).filter(CartModel.cno == cno).first()
        if db_cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        for key, value in cart.dict().items():
            setattr(db_cart, key, value)

        db.commit()
        db.refresh(db_cart)
        return db_cart

    @staticmethod
    def delete_cart_item(db: Session, cno: int):
        db_cart = db.query(CartModel).filter(CartModel.cno == cno).first()
        if db_cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

        db.delete(db_cart)
        db.commit()
        return db_cart
