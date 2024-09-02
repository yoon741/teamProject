from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.product import Product as ProductModel

shop_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@shop_router.get("/item_gallery", response_class=HTMLResponse)
async def item_gallery(request: Request, db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return templates.TemplateResponse("shop/item_gallery.html", {"request": request, "products": products})

@shop_router.get("/item_detail/{prdno}", response_class=HTMLResponse)
async def item_detail(request: Request, prdno: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()

    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return templates.TemplateResponse("shop/item_detail.html", {
        "request": request,
        "product": product
    })
