from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.product import Product as ProductModel

menu_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

shop_router = APIRouter()

# shop 라우터 제품번호에 따른 엔드포인트 지정
# 관리자입장 / 회원입장 라우트 된 엔드포인트가 달라야 한다

# ex)
# member/product/{prdno}
# admin/product/{prdno}
@shop_router.get("/item_gallery", response_class=HTMLResponse)
async def item_gallery(request: Request, db: Session = Depends(get_db)):
    # 모든 상품 목록을 DB에서 가져옵니다.
    products = db.query(ProductModel).all()

    # 상품의 가격을 리스트로 추출합니다.
    prices = [product.price for product in products]

    # 템플릿에 필요한 데이터를 전달합니다.
    return templates.TemplateResponse("shop/item_gallery.html", {
        "request": request,
        "prices": prices
    })


@shop_router.get("/item_detail/{prdno}", response_class=HTMLResponse)
async def item_detail(request: Request, prdno: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()

    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return templates.TemplateResponse("shop/item_detail.html", {
        "request": request,
        "product": product
    })
