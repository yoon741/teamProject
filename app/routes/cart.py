from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from app.model.cart import Cart as CartModel
from app.model.product import Product as ProductModel


cart_router = APIRouter()

@cart_router.post("/add")
async def add_to_cart(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    product_id = data.get('prdno')
    qty = data.get('qty')

    user_id = request.session.get("userid")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized: Please log in to add items to the cart.")

    # 상품 정보 조회
    product = db.query(ProductModel).filter(ProductModel.prdno == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < qty:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # 장바구니에 동일한 상품이 있는지 확인
    cart_item = db.query(CartModel).filter(CartModel.mno == user_id, CartModel.prdno == product_id).first()

    if cart_item:
        # 기존 장바구니 항목 업데이트
        cart_item.qty += qty
        cart_item.price += product.price * qty
    else:
        # 새로운 장바구니 항목 추가
        cart_item = CartModel(mno=user_id, prdno=product_id, qty=qty, price=product.price * qty)
        db.add(cart_item)

    db.commit()
    return {"message": "Item added to cart successfully"}
