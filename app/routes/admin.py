from typing import List

from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import Form
from app.dbfactory import get_db
from app.model.member import Member
from app.model.product import Product, PrdAttach
from app.schema.product import NewProduct
from app.service.product import ProductService
from app.model.product import Product as ProductModel
from app.model.order import Order

admin_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

async def require_admin(req: Request):
    userid = req.session.get('userid')
    is_admin = req.session.get('is_admin')

    if not userid or not is_admin:
        return RedirectResponse(url='/', status_code=303)
    return None

@admin_router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/admin.html", {"request": req})

@admin_router.get("/mgproduct", response_class=HTMLResponse)
async def mgproduct(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    products = db.query(Product).all()
    return templates.TemplateResponse("admin/mgproduct.html", {"request": req, "products": products})

@admin_router.post('/rgproduct', response_class=HTMLResponse)
async def rgproductok(req: Request, product: NewProduct = Depends(ProductService.get_product_data),
                      files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    try:
        attachs = await ProductService.process_upload(files)
        if ProductService.insert_product(product, attachs, db):
            return RedirectResponse('/admin/mgproduct', status_code=303)
    except Exception as ex:
        print(f'▷▷▷ rgproductok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error', status_code=303)

# 회원 관리 페이지
# 회원 관리 페이지
@admin_router.get("/mguser", response_class=HTMLResponse)
async def mguser(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    members = db.query(Member).all()  # 모든 회원 정보 가져오기
    return templates.TemplateResponse("admin/mguser.html", {"request": req, "member": members})


@admin_router.get("/mgorder", response_class=HTMLResponse)
async def mgorder(req: Request, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    orders = db.query(Order).all()
    return templates.TemplateResponse("admin/mgorder.html", {"request": req, "orders": orders})

@admin_router.get("/rgproduct", response_class=HTMLResponse)
async def rgproduct(req: Request):
    response = await require_admin(req)
    if response:
        return response
    return templates.TemplateResponse("admin/rgproduct.html", {"request": req})

@admin_router.get("/shop/item_detail/{prdno}", response_class=HTMLResponse)
async def item_detail(req: Request, prdno: int, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    product = db.query(Product).filter(Product.prdno == prdno).first()
    if not product:
        return RedirectResponse('/404', status_code=404)
    return templates.TemplateResponse("shop/item_detail.html", {"request": req, "product": product})

@admin_router.delete("/deleteproduct/{prdno}")
async def delete_product(req: Request, prdno: int, db: Session = Depends(get_db)):
    response = await require_admin(req)
    if response:
        return response
    product = db.query(ProductModel).filter(ProductModel.prdno == prdno).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    db.query(PrdAttach).filter(PrdAttach.prdno == prdno).delete()
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
    return templates.TemplateResponse("admin/editproduct.html", {"request": req, "product": product})

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
        existing_product.prdname = product.prdname
        existing_product.price = product.price
        existing_product.type = product.type
        existing_product.qty = product.qty
        existing_product.description = product.description

        if files:
            attachs = await ProductService.process_upload(files)

        db.commit()
        return RedirectResponse('/admin/mgproduct', status_code=303)
    except Exception as ex:
        print(f'상품 수정 오류 발생: {str(ex)}')
        return RedirectResponse('/member/error', status_code=303)