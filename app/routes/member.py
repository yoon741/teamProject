from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.member import Member
from app.schema.member import NewMember
from app.service.member import MemberService
from pydantic import ValidationError

member_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@member_router.get("/join", response_class=HTMLResponse)
async def join(req: Request):
    return templates.TemplateResponse("member/join.html", {"request": req})

@member_router.post("/join", response_class=HTMLResponse)
async def joinok(req: Request, db: Session = Depends(get_db)):
    try:
        data = await req.json()
        if MemberService.is_userid_taken(db, data["userid"]):
            return JSONResponse(status_code=400, content={"message": "이미 사용 중인 아이디입니다."})
        new_member = NewMember(**data)
        MemberService.insert_member(db, new_member)
        print(f"[INFO] New member inserted: {new_member.userid}")
        return RedirectResponse(url='/member/login', status_code=303)
    except Exception as ex:
        print(f'[ERROR] 회원가입 오류: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get("/login", response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse("member/login.html", {"request": req})

@member_router.post("/login", response_class=HTMLResponse)
async def loginok(req: Request, db: Session = Depends(get_db)):
    try:
        form_data = await req.form()
        userid = form_data.get("userid")
        password = form_data.get("password")

        user = MemberService.login_member(db, {"userid": userid, "password": password})
        if user:
            req.session['userid'] = userid
            print(f"[INFO] User logged in: {userid}")
            next_url = req.query_params.get("next", "/")
            return RedirectResponse(url=next_url, status_code=303)
        else:
            print("[WARNING] Login failed: Invalid username or password")
            return RedirectResponse(url='/member/loginfail', status_code=303)
    except ValidationError as e:
        errors = e.errors()
        return JSONResponse(status_code=422, content={"errors": errors})
    except Exception as ex:
        print(f'[ERROR] 로그인 오류: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get("/myinfo", response_class=HTMLResponse)
async def myinfo(req: Request, db: Session = Depends(get_db)):
    try:
        userid = req.session.get('userid')
        if not userid:
            return RedirectResponse(url='/member/login', status_code=303)

        user = db.query(Member).filter(Member.userid == userid).first()
        if user is None:
            return RedirectResponse(url='/member/loginfail', status_code=303)

        print(f"[INFO] Fetched info for user: {userid}")
        return templates.TemplateResponse("member/myinfo.html", {"request": req, "user": user})
    except Exception as ex:
        print(f'[ERROR] 회원 정보 페이지 오류: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.post("/modify", response_class=HTMLResponse)
async def modify_user_info(req: Request, db: Session = Depends(get_db)):
    try:
        form_data = await req.form()
        userid = req.session.get('userid')

        if not userid:
            return RedirectResponse(url='/member/login', status_code=303)

        user = db.query(Member).filter(Member.userid == userid).first()

        if user:
            if 'password' in form_data and form_data.get('password'):
                user.password = MemberService.sha256_hash(form_data.get('password'))
                print(f"[INFO] Password updated for user: {userid}")

            user.email = form_data.get('email')
            user.phone = form_data.get('phone')
            user.address = form_data.get('address')
            print(f"[INFO] User information updated for user: {userid}")

            db.commit()
            return HTMLResponse(content="Success", status_code=200)
        else:
            print("[WARNING] User not found during update")
            return HTMLResponse(content="User not found", status_code=404)

    except Exception as ex:
        db.rollback()
        print(f'[ERROR] 업데이트 오류: {str(ex)}')
        return HTMLResponse(content="Error", status_code=500)

@member_router.get("/logout", response_class=HTMLResponse)
async def logout(req: Request):
    req.session.clear()
    print(f"[INFO] User logged out")
    return RedirectResponse(url='/', status_code=303)

@member_router.get("/error", response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse("member/error.html", {"request": req})
