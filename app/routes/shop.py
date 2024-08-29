from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

menu_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

shop_router = APIRouter()

# shop 라우터 제품번호에 따른 엔드포인트 지정
# 관리자입장 / 회원입장 라우트 된 엔드포인트가 달라야 한다

# ex)
# member/product/{prdno}
# admin/product/{prdno}
@shop_router.get("/item_detail", response_class=HTMLResponse)
async def item_detail(request: Request):
    return templates.TemplateResponse("shop/item_detail.html", {"request": request})


@shop_router.get("/item_gallery", response_class=HTMLResponse)
async def item_gallery(request: Request):
    return templates.TemplateResponse("shop/item_gallery.html", {"request": request})