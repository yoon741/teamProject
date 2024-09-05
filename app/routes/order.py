from fastapi import APIRouter, Depends, HTTPException, status, Form
from typing import List
from sqlalchemy import func, select
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

@order_router.post("/setsession")
async def set_session(request: Request, db: Session = Depends(get_db)):
    # 세션에서 userid를 가져와서 데이터베이스에서 사용자 정보 조회
    userid = request.session.get("userid")

    # 로그인 여부 확인
    if not userid:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized. Please login first."})

    # 데이터베이스에서 사용자 정보 조회
    member = db.query(Member).filter(Member.userid == userid).first()

    if not member:
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    # 클라이언트로부터 상품 정보 받음
    data = await request.json()

    # 상품 정보 조회
    product = db.query(ProductModel).filter(ProductModel.prdno == data['prdno']).first()

    if not product:
        return JSONResponse(status_code=404, content={"detail": "Product not found"})

    # 세션에 제품 정보 저장
    request.session['product_info'] = {
        'prdno': product.prdno,
        'prdname': product.prdname,
        'qty': data['qty'],
        'price': product.price
    }

    # 세션에 member_info 저장
    request.session['member_info'] = {
        'mno': member.mno,
        'username': member.username,
        'email': member.email,
        'phone': member.phone,
        'address': member.address,
        'postcode': member.postcode
    }

    # 세션에 저장된 값 확인 (디버깅용 출력)
    print("Session after storing member_info:", request.session.get("member_info"))

    # 세션에서 member_info 가져오기
    member_info = request.session.get("member_info")

    if member_info:
        mno = member_info.get('mno')  # 세션에서 mno를 가져오기
        print("User mno from session:", mno)
    else:
        print("No member_info found in session")

    # 세션에 저장된 product_info도 확인
    print("Session product info:", request.session.get("product_info"))

    # 디버깅용으로 logged-in 유저 정보도 확인
    print("Logged-in user info:", request.session.get("member_info"))

    return JSONResponse(content={"success": True})



@order_router.get("/sessionorder", response_class=HTMLResponse)
async def session_order(req: Request, db: Session = Depends(get_db)):
    # 세션에서 제품 정보 가져오기
    product_info = req.session.get("product_info")
    member_info = req.session.get("member_info")

    # 세션 정보 디버깅 로그 추가
    print(f"Product info: {product_info}")
    print(f"Member info: {member_info}")

    # 세션에 정보가 없으면 상품 페이지로 리다이렉트
    if not product_info or not member_info:
        return RedirectResponse(url="/shop/item_gallery")

    # 총 가격 계산
    total_price = int(product_info['price']) * int(product_info['qty'])

    # 템플릿에 정보 전달
    return templates.TemplateResponse("order/sessionorder.html", {
        "request": req,
        "product_info": product_info,
        "member_info": member_info,
        "total_price": total_price
    })


@order_router.post("/sessionorderok", response_class=HTMLResponse)
async def session_order_ok(req: Request, payment: str = Form(...), db: Session = Depends(get_db)):
    # 세션에서 제품 정보와 회원 정보 가져오기
    product_info = req.session.get("product_info")
    member_info = req.session.get("member_info")

    if not product_info or not member_info:
        # 세션에 정보가 없으면 오류 처리 또는 리다이렉트
        return RedirectResponse(url="/shop/item_gallery", status_code=302)

    # 총 결제 금액 계산
    total_price = int(product_info['price']) * int(product_info['qty'])

    # 주문 정보를 데이터베이스에 저장
    try:
        stmt = select(func.coalesce(func.max(Order.omno), 0) + 1)
        new_omno = db.execute(stmt).scalar()

        new_order = Order(
            omno=new_omno,
            mno=member_info['mno'],  # 회원 번호
            prdno=product_info['prdno'],  # 제품 번호
            qty=int(product_info['qty']),  # 수량
            price=int(product_info['price']),  # 단가
            postcode=member_info['postcode'],  # 우편번호
            addr=member_info['address'],  # 주소
            phone=member_info['phone'],  # 전화번호
            payment=payment  # 결제 방법
        )

        db.add(new_order)
        db.commit()

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": "Failed to save order: " + str(e)})

    # 결제 완료 후 세션에서 제품 정보 삭제
    del req.session["product_info"]

    # 주문한 상품 정보 구성
    order_items = [{
        "product_name": product_info['prdname'],
        "quantity": product_info['qty'],
        "price": product_info['price']
    }]

    # 결제 완료 페이지 렌더링
    return templates.TemplateResponse("order/sessionorderok.html", {
        "request": req,
        "order_id": new_omno,
        "customer_name": member_info['username'],
        "shipping_address": member_info['address'],
        "contact_number": member_info['phone'],
        "email": member_info['email'],
        "order_items": order_items,
        "total_price": total_price,
        "product_info": product_info  # 템플릿에 product_info 전달
    })



