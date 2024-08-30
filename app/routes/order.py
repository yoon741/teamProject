from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.service.cart import CartService
from app.service.product import ProductService
from app.service.order import OrderService  # 추가: OrderService 가정

order_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@order_router.get("/order", response_class=HTMLResponse)
async def order(req: Request, db: Session = Depends(get_db)):
    if 'userid' not in req.session:
        return RedirectResponse(url=f"/member/login?next=/order")

    return templates.TemplateResponse("order/order.html", {"request": req})

# 카트에서 주문페이지로 데이터 넘김
@order_router.post("/cart/order", response_class=HTMLResponse)
async def order_from_cart(req: Request, db: Session = Depends(get_db)):
    if 'userid' not in req.session:
        return RedirectResponse(url=f"/member/login?next=/cart/order")

    try:
        userid = req.session['userid']
        cart_items = CartService.get_cart_items_by_userid(db, userid)

        if not cart_items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items in cart")

        return templates.TemplateResponse("order/order.html", {"request": req, "cart_items": cart_items})

    except Exception as e:
        print(f"Error processing order from cart: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your order")

# 상품디테일에서 주문페이지로 데이터 넘김
@order_router.post("/product/{prdno}/order", response_class=HTMLResponse)
async def order_from_product(req: Request, prdno: int, db: Session = Depends(get_db)):
    if 'userid' not in req.session:
        return RedirectResponse(url=f"/member/login?next=/product/{prdno}/order")

    try:
        product = ProductService.get_product_detail(db, prdno)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        return templates.TemplateResponse("order/order.html", {"request": req, "product": product})

    except Exception as e:
        print(f"Error processing order from product: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your order")

# 주문 완료 페이지
@order_router.get("/orderok", response_class=HTMLResponse)
async def orderok(req: Request):
    if 'userid' not in req.session:
        return RedirectResponse(url="/member/login?next=/orderok")

    return templates.TemplateResponse("order/orderok.html", {"request": req})

# 나의 주문 페이지
@order_router.get("/myorder", response_class=HTMLResponse)
async def myorder(req: Request, db: Session = Depends(get_db)):
    if 'userid' not in req.session:
        return RedirectResponse(url="/member/login?next=/myorder")

    userid = req.session['userid']
    try:
        orders = OrderService.get_orders_by_userid(db, userid)
        return templates.TemplateResponse("order/myorder.html", {"request": req, "orders": orders})

    except Exception as e:
        print(f"Error fetching user orders: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching your orders")
