from typing import List

from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.model.member import Member
from app.model.product import Product, PrdAttach
from app.schema.product import NewProduct
from app.service.product import ProductService
from starlette.responses import HTMLResponse
from app.dbfactory import get_db
from app.model.product import Product as ProductModel

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
async def mgproduct(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    # 모든 상품 정보를 가져옵니다.
    products = db.query(Product).all()

    # 템플릿에 제품 목록을 전달합니다.
    return templates.TemplateResponse("admin/mgproduct.html", {"request": req, "products": products})


@admin_router.post('/rgproduct', response_class=HTMLResponse)
async def rgproductok(req: Request, product: NewProduct = Depends(ProductService.get_product_data),
                      files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    try:
        print(product)
        attachs = await ProductService.process_upload(files)
        print(attachs)
        if ProductService.insert_product(product, attachs, db):
            # 등록이 성공하면 상품 관리 페이지로 리다이렉션
            return RedirectResponse('/admin/mgproduct', status_code=303)
    except Exception as ex:
        print(f'▷▷▷ rgproductok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error', status_code=303)



# 회원 관리 페이지
@admin_router.get("/mguser", response_class=HTMLResponse)
async def mguser(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    # 모든 회원 정보를 가져옵니다.
    member = db.query(Member).all()

    return templates.TemplateResponse("admin/mguser.html", {"request": req, "member": member})

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
    response = await require_admin(req)
    if response:
        return response
    try:
        print(product)
        attachs = await ProductService.process_upload(files)
        print(attachs)
        if ProductService.insert_product(product, attachs, db):
            return RedirectResponse('/shop/item_gallery', 303)

    except Exception as ex:
        print(f'▷▷▷ rgproductok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error', 303)


@admin_router.get("/shop/item_detail/{prdno}", response_class=HTMLResponse)
async def item_detail(req: Request, prdno: int, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    # 상품 ID를 이용하여 상품 정보를 가져옴
    product = db.query(Product).filter(Product.prdno == prdno).first()

    # 상품이 존재하지 않을 경우 404 에러 처리
    if not product:
        return RedirectResponse('/404', status_code=404)

    # 상품 정보를 템플릿에 전달하여 렌더링
    return templates.TemplateResponse("shop/item_detail.html", {"request": req, "product": product})



@admin_router.delete("/deleteproduct/{prdno}")
async def delete_product(req: Request, prdno: int, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()

    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    # 먼저 연관된 PrdAttach 데이터를 삭제합니다.
    db.query(PrdAttach).filter(PrdAttach.prdno == prdno).delete()

    # 그 후 상품을 삭제합니다.
    db.delete(product)
    db.commit()

    return {"message": "상품이 성공적으로 삭제되었습니다."}


@admin_router.get("/editproduct/{prdno}", response_class=HTMLResponse)
async def edit_product(req: Request, prdno: int, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()

    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return templates.TemplateResponse("admin/editproduct.html", {
        "request": req,
        "product": product
    })


@admin_router.post("/editproduct/{prdno}", response_class=HTMLResponse)
async def update_product(req: Request, prdno: int, product: NewProduct = Depends(ProductService.get_product_data),
                         files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    try:
        existing_product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()

        if not existing_product:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

        # 기존 상품 데이터 업데이트
        existing_product.prdname = product.prdname
        existing_product.price = product.price
        existing_product.type = product.type
        existing_product.qty = product.qty
        existing_product.description = product.description

        # 파일 처리 및 추가 작업
        if files:
            attachs = await ProductService.process_upload(files)
            # 기존 파일 삭제 및 새 파일 추가 처리 필요

        db.commit()

        return RedirectResponse('/admin/mgproduct', status_code=303)
    except Exception as ex:
        print(f'상품 수정 오류 발생: {str(ex)}')
        return RedirectResponse('/member/error', status_code=303)
