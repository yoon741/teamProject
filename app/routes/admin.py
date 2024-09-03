from typing import List

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.model.member import Member
from app.schema.product import NewProduct
from app.service.product import ProductService


# 라우터와 템플릿 설정
admin_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 공통 접근 제어 로직
async def require_admin(req: Request):
    """
    관리자 권한이 필요한 페이지에 접근하기 위한 공통 접근 제어 함수
    """
    userid = req.session.get('userid')
    is_admin = req.session.get('is_admin')

    if not userid or not is_admin:
        return RedirectResponse(url='/', status_code=303)

    return None

# 관리자 페이지 (메인)
@admin_router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/admin.html", {"request": req})

# 상품 관리 페이지
@admin_router.get("/mgproduct", response_class=HTMLResponse)
async def mgproduct(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/mgproduct.html", {"request": req})

# 회원 관리 페이지
@admin_router.get("/mguser", response_class=HTMLResponse)
async def mguser(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response

    # 모든 회원 정보를 가져옵니다.
    members = db.query(Member).all()
    return templates.TemplateResponse("admin/mguser.html", {"request": req, "members": members})

# 주문 관리 페이지
@admin_router.get("/mgorder", response_class=HTMLResponse)
async def mgorder(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/mgorder.html", {"request": req})

# 상품 등록 페이지
@admin_router.get("/rgproduct", response_class=HTMLResponse)
async def rgproduct(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/rgproduct.html", {"request": req})

@admin_router.post('/rgproduct', response_class=HTMLResponse)
async def rgproductok(req: Request, product: NewProduct = Depends(ProductService.get_product_data),
                      files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        print(product)
        attachs = await ProductService.process_upload(files)
        print(attachs)
        if ProductService.insert_product(product, attachs, db):
            return RedirectResponse('/shop/item_gallery', 303)

    except Exception as ex:
        print(f'▷▷▷ rgproductok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error', 303)