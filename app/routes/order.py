from fastapi import APIRouter, Depends, HTTPException, status, Form
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.model.member import Member
from app.service.cart import CartService
from app.service.product import ProductService
from app.service.order import OrderService
from app.model.order import Order
from app.schema.order import OrderRead
from app.model.product import Product as ProductModel, Product

order_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

def check_login(req: Request):
    if 'userid' not in req.session:
        return False
    return True


@order_router.post("/orderok", response_class=HTMLResponse)
def orderok(
        req: Request,
        mno: int = Form(...),
        prdno: List[int] = Form(...),
        qty: List[int] = Form(...),
        price: List[int] = Form(...),
        postcode: str = Form(...),
        addr: str = Form(...),
        phone: str = Form(...),
        payment: str = Form(...),
        db: Session = Depends(get_db)
):
    # 주문 정보 처리
    member = db.query(Member).filter(Member.mno == mno).first()

    if not member:
        raise HTTPException(status_code=404, detail="User not found")

    # 주문 번호 생성
    order_number = db.query(func.max(Order.omno)).scalar() + 1 if db.query(func.count(Order.omno)).scalar() > 0 else 1

    # 다중 제품 처리
    for i in range(len(prdno)):
        order = Order(
            omno=order_number,
            mno=mno,
            prdno=prdno[i],
            qty=qty[i],
            price=price[i],
            postcode=postcode,
            addr=addr,
            phone=phone,
            payment=payment
        )
        db.add(order)

    db.commit()

    # 결제된 상품 장바구니에서 제거
    CartService.clear_cart_items(db, member.userid)  # CartService에서 해당 사용자 장바구니를 비웁니다.

    # 주문 완료 페이지 렌더링
    return templates.TemplateResponse("order/orderok.html", {
        "request": req,
        "order_id": order_number,
        "customer_name": member.username,
        "shipping_address": addr,
        "contact_number": phone,
        "email": member.email,
        "order_items": [{"product_name": db.query(ProductModel).filter(ProductModel.prdno == prdno[i]).first().prdname,
                         "quantity": qty[i],
                         "price": price[i]} for i in range(len(prdno))],
        "total_price": sum(price[i] * qty[i] for i in range(len(prdno)))
    })



def generate_payment_info(payment_method: str, member: Member):
    if payment_method == "bank_transfer":
        return f"무통장 입금 - 계좌번호 : {member.phone} 입금자명 : {member.username}"
    elif payment_method == "kakao":
        return "카카오페이"
    elif payment_method == "naver":
        return "네이버페이"
    else:
        return "기타"

@order_router.get("/order/{omno}", response_class=HTMLResponse)
def read_order(omno: int, db: Session = Depends(get_db)):
    order = OrderService.get_order(db, omno)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@order_router.get("/order", response_class=HTMLResponse)
async def order(req: Request, db: Session = Depends(get_db)):
    if not check_login(req):
        return RedirectResponse(url=f"/member/login?next=/order")

    userid = req.session.get('userid')
    member_info = db.query(Member).filter(Member.userid == userid).first()

    # 세션에 단일 제품 정보가 있는지 확인
    if "product_info" in req.session:
        product_info = req.session["product_info"]
        product = db.query(ProductModel).filter(ProductModel.prdno == product_info["prdno"]).first()
        total_price = product_info["price"] * product_info["qty"]
        cart_items = []
    else:
        # 세션에 단일 제품 정보가 없으면 기존 장바구니 항목을 처리
        product = None
        cart_items = CartService.get_cart_items_by_userid(db, userid)
        total_price = sum(item.price * item.qty for item in cart_items)

    return templates.TemplateResponse("order/order.html", {
        "request": req,
        "member_info": member_info,
        "product": product,
        "total_price": total_price,
        "cart_items": cart_items
    })


@order_router.post("/product/{prdno}/order", response_class=HTMLResponse)
async def order_from_product(req: Request, prdno: int, db: Session = Depends(get_db)):
    if not check_login(req):
        return RedirectResponse(url=f"/member/login?next=/product/{prdno}/order")

    try:
        product = ProductService.get_product_detail(db, prdno)
        userid = req.session['userid']
        member_info = OrderService.get_member_info(db, userid)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        total_price = product.price
        req.session["product_info"] = {"prdno": prdno, "price": total_price}

        return RedirectResponse(url="/order", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing your order")

@order_router.get("/myorder", response_class=HTMLResponse)
async def myorder(req: Request, db: Session = Depends(get_db)):
    if not check_login(req):
        return RedirectResponse(url="/member/login?next=/myorder")

    userid = req.session['userid']
    member = db.query(Member).filter(Member.userid == userid).first()
    orders = db.query(Order).filter(Order.mno == member.mno).order_by(Order.regdate.desc()).all()

    return templates.TemplateResponse("order/myorder.html", {"request": req, "orders": orders})

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/set-session")
async def set_session(request: Request):
    try:
        data = await request.json()
        prdno = data.get('prdno')
        price = data.get('price')
        qty = data.get('qty')

        request.session['order'] = {
            'prdno': prdno,
            'price': price,
            'qty': qty
        }

        return JSONResponse(content={"success": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to set session")

