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
async def item_gallery(request: Request, category: str = None, db: Session = Depends(get_db)):
    try:
        # 선택된 카테고리에 따라 상품 필터링
        prdlist = ProductService.select_product(db, category)

        return templates.TemplateResponse('shop/item_gallery.html', {
            'request': request,
            'prdlist': prdlist,
            'selected_category': category  # 선택된 카테고리를 템플릿에 전달
        })
    except Exception as ex:
        print(f'▶▶▶item_gallery 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


def categorize_product(type):
    if '의자' in type:
        return '의자'
    elif '테이블' in type:
        return '테이블'
    elif '소파' in type:
        return '소파'
    else:
        return '기타'

@shop_router.get("/shop", response_class=HTMLResponse)
async def show_products(request: Request, db: Session = Depends(get_db), category: str = None):
    # 기본 쿼리 생성
    query = db.query(Product)

    # 카테고리 필터링
    if category:
        if category == "기타":
            # 의자, 테이블, 소파가 아닌 상품들만 가져옴
            query = query.filter(~Product.type.in_(["의자", "테이블", "소파"]))
        else:
            # 지정된 카테고리에 해당하는 상품만 가져옴
            query = query.filter(Product.type == category)

    # 필터링된 상품을 가져옴
    products = query.all()

    # 상품 목록을 템플릿에 전달할 데이터로 변환
    categorized_products = []
    for product in products:
        categorized_products.append({
            "prdno": product.prdno,
            "prdname": product.prdname,
            "price": product.price,
            "image_url": product.image_url,  # 이미지 URL도 필요하다면 추가
            "type": product.type
        })

    # 템플릿에 데이터를 전달하여 렌더링
    return templates.TemplateResponse("shop.html", {
        "request": request,
        "products": categorized_products
    })

