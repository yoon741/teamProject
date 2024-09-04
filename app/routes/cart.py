from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from app.dbfactory import get_db
from app.model.product import Cart as CartModel, Cart, Product
from app.model.product import Product as ProductModel
from app.model.member import Member
from app.routes.shop import templates

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

    member = db.query(Member).filter(Member.userid == userid).first()
    if not member:
        raise HTTPException(status_code=404, detail="회원 정보를 찾을 수 없습니다.")

    mno = member.mno

    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    if product.qty < qty:
        raise HTTPException(status_code=400, detail="재고가 부족합니다.")

    cart_item = db.query(CartModel).filter(CartModel.mno == mno, CartModel.prdno == prdno).first()

    if cart_item:
        cart_item.qty += qty
        cart_item.price += product.price * qty
    else:
        cart_item = CartModel(mno=mno, prdno=prdno, qty=qty, price=product.price * qty)
        db.add(cart_item)

    product.qty -= qty
    db.commit()

    return {"message": "장바구니에 추가되었습니다."}

from sqlalchemy.orm import joinedload

@cart_router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, db: Session = Depends(get_db)):
    userid = request.session.get("userid")

    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    member = db.query(Member).filter(Member.userid == userid).first()
    if not member:
        raise HTTPException(status_code=404, detail="회원 정보를 찾을 수 없습니다.")

    mno = member.mno

    # 장바구니 항목과 연관된 상품과 첨부 파일을 함께 로드
    cart_items = db.query(Cart).options(
        joinedload(Cart.product).joinedload(Product.attachs)
    ).filter(Cart.mno == mno).all()

    if not cart_items:
        return templates.TemplateResponse("shop/cart.html", {
            "request": request,
            "cart_items": [],
            "total_price": 0
        })

    total_price = sum(item.price * item.qty for item in cart_items)

    return templates.TemplateResponse("shop/cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total_price": total_price
    })


@cart_router.delete("/remove/{cno}")
async def remove_item_from_cart(cno: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartModel).filter(CartModel.cno == cno).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="장바구니에서 해당 항목을 찾을 수 없습니다.")

    try:
        db.delete(cart_item)
        db.commit()
        return {"message": "장바구니에서 항목이 제거되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="장바구니에서 항목을 제거하는 중 오류가 발생했습니다.")

@cart_router.put("/update/{cno}")
async def update_cart_item(cno: int, qty: int, db: Session = Depends(get_db)):
    cart_item = db.query(CartModel).filter(CartModel.cno == cno).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="장바구니에서 해당 항목을 찾을 수 없습니다.")

    if qty <= 0:
        raise HTTPException(status_code=400, detail="수량은 1 이상이어야 합니다.")

    try:
        product = db.query(ProductModel).filter(ProductModel.prdno == cart_item.prdno).first()
        if not product:
            raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")

        if product.qty + cart_item.qty < qty:
            raise HTTPException(status_code=400, detail="재고가 부족합니다.")

        product.qty += cart_item.qty
        cart_item.qty = qty
        cart_item.price = qty * product.price
        product.qty -= qty

        db.commit()
        return {"message": "장바구니 항목이 업데이트되었습니다."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="장바구니 항목을 업데이트하는 중 오류가 발생했습니다.")


