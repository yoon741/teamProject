from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

order_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 주문 페이지 (메인)
@order_router.get("/order", response_class=HTMLResponse)
async def order(req: Request):
    return templates.TemplateResponse("order/order.html", {"request": req})

# 상품 관리 페이지
@order_router.get("/orderok", response_class=HTMLResponse)
async def orderok(req: Request):
    return templates.TemplateResponse("order/orderok.html", {"request": req})

@order_router.get("/myorder", response_class=HTMLResponse)
async def myorder(req: Request):
    return templates.TemplateResponse("order/myorder.html", {"request": req})
