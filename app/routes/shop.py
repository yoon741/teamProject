from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.product import PrdAttach, Product
from app.service.product import ProductService

shop_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@shop_router.get("/item_detail/{prdno}", response_class=HTMLResponse)
async def item_detail(request: Request, prdno: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.prdno == prdno).first()
        prdattach = db.query(PrdAttach).filter(PrdAttach.prdno == prdno).first()

        if not product:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

        return templates.TemplateResponse("shop/item_detail.html", {
            "request": request,
            "product": product,
            "prdattach": prdattach
        })

    except Exception as ex:
        print(f'▶▶▶item_detail 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@shop_router.get('/item_gallery', response_class=HTMLResponse)
async def item_gallery(req: Request, prdno: int = None, db: Session = Depends(get_db)):
    try:
        prdlist = ProductService.select_product(db)
        product = db.query(Product).filter(Product.prdno == prdno).first() if prdno else None
        prdattach = db.query(PrdAttach).filter(PrdAttach.prdno == prdno).first() if prdno else None
        print(prdlist)
        return templates.TemplateResponse('shop/item_gallery.html', {
            'request': req, 'prdlist': prdlist,
            "product": product, "prdattach": prdattach
        })
    except Exception as ex:
        print(f'▶▶▶item_gallery 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

