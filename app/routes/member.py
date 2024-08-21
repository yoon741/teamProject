from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.member import NewMember
from app.service.member import MemberService

member_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@member_router.get("/join", response_class=HTMLResponse)
async def join(request: Request):
    return templates.TemplateResponse("member/join.html", {"request": request})

@member_router.post("/join", response_class=HTMLResponse)
async def joinok(member: NewMember, db: Session = Depends(get_db)):
    try:
        # 캡챠가 참이라면
        if MemberService.check_captcha(member):
            print(member)
            result = MemberService.insert_member(db, member)
            print('처리결과: ', result.rowcount)

            #회원가입이 성공적으로 완료되면 로그인페이지로 전환
            if result.rowcount > 0: #rowcount 변경된 행이 1개 이상이면 실행 = 회원가입 잘했으면 실행
                return RedirectResponse(url='/member/login', status_code=303)
        # 캡챠 실패시 에러
        else:
            return RedirectResponse(url='/member/error', status_code=303)

    except Exception as ex:
        print(f'▷▷▷ joinok 오류발생: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("member/login.html", {"request": request})

@member_router.get("/myinfo", response_class=HTMLResponse)
async def myinfo(request: Request):
    return templates.TemplateResponse("member/myinfo.html", {"request": request})

@member_router.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse("member/error.html", {"request": request})



# 엔드포인트 설정