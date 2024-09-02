from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.model.member import Member

admin_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 관리자 페이지 (메인)
@admin_router.get("/admin", response_class=HTMLResponse)
async def adminok(req: Request):
    return templates.TemplateResponse("admin/admin.html", {"request": req})

# 상품 관리 페이지
@admin_router.get("/mgproduct", response_class=HTMLResponse)
async def mgproduct(req: Request):
    return templates.TemplateResponse("admin/mgproduct.html", {"request": req})

# 회원 관리 페이지
@admin_router.get("/mguser", response_class=HTMLResponse)
async def mguser(req: Request, db: Session = Depends(get_db)):
    userid = req.session.get('userid')
    is_admin = req.session.get('is_admin')

    # 관리자가 아닌 경우 접근 불가
    if not userid or not is_admin:
        return RedirectResponse(url='/', status_code=303)

    # 모든 회원 정보를 가져옵니다.
    member = db.query(Member).all()

    return templates.TemplateResponse("admin/mguser.html", {"request": req, "member": member})

# 주문 관리 페이지
@admin_router.get("/mgorder", response_class=HTMLResponse)
async def mgorder(req: Request):
    return templates.TemplateResponse("admin/mgorder.html", {"request": req})

# 상품 등록 페이지
@admin_router.get("/rgproduct", response_class=HTMLResponse)
async def rgproduct(req: Request):
    return templates.TemplateResponse("admin/rgproduct.html", {"request": req})