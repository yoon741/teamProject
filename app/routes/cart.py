from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from app.routes.shop import templates

from app.dbfactory import get_db
from app.model.product import Cart as CartModel
from app.model.product import Product as ProductModel

# APIRouter를 인스턴스화
cart_router = APIRouter()

@cart_router.post("/add")
async def add_to_cart(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    prdno = data.get('prdno')
    qty = data.get('qty')

    try:
        qty = int(qty)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 수량입니다.")

    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    if product.qty < qty:
        raise HTTPException(status_code=400, detail="재고가 부족합니다.")

    cart_item = db.query(CartModel).filter(CartModel.mno == userid, CartModel.prdno == prdno).first()

    if cart_item:
        cart_item.qty += qty
        cart_item.price += int(product.price.replace("₩", "").replace(",", "")) * qty
    else:
        cart_item = CartModel(mno=userid, prdno=prdno, qty=qty, price=int(product.price.replace("₩", "").replace(",", "")) * qty)
        db.add(cart_item)

    product.qty -= qty
    db.commit()

    return {"message": "장바구니에 추가되었습니다."}


@cart_router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, db: Session = Depends(get_db)):
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # 장바구니 항목 가져오기 (Product 정보 포함)
    cart_items = db.query(CartModel).filter(CartModel.mno == userid).all()

    if not cart_items:
        return templates.TemplateResponse("shop/cart.html", {"request": request, "cart_items": [], "total_price": 0})

    total_price = sum(item.price * item.qty for item in cart_items)

    return templates.TemplateResponse("shop/cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total_price": total_price
    })
