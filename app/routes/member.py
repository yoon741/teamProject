#기존 수업 member

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
async def join(req: Request):
    return templates.TemplateResponse("member/join.html", {"request": req})

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
    # 이외 오류 뜨면 실행
    except Exception as ex:
        print(f'▷▷▷ joinok 오류발생: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get("/login", response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse("member/login.html", {"request": req})

@member_router.post("/login", response_class=HTMLResponse)
async def loginok(req: Request, db: Session = Depends(get_db)):
    # 클라이언트가 보낸 데이터를 request 객체로 받음
    data = await req.json()
    try:
        print('전송한 데이터 : ', data)
        redirect_url = '/member/loginfail' #로그인 실패시 loginfail 로 이동

        # M.서비스에서 쿼리문으로 판별할거임 거기서 T/F 값 여기로 받는다 생각하면 될 듯
        if MemberService.login_member(db, data):    #로그인 성공시 myinfo로 이동
            req.session['logined_uid'] = data.get('userid') # 세션에 아이디 저장하고
            redirect_url = '/member/myinfo'

        return RedirectResponse(url=redirect_url, status_code=303)

    except Exception as ex:
        print(f'▶▶▶ loginok 오류: {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@member_router.get("/logout", response_class=HTMLResponse)
async def logout(req: Request):
    req.session.clear() # 생성된 세션 객체 제거
    return RedirectResponse("/", status_code=303)

@member_router.get('/myinfo', response_class=HTMLResponse)
async def myinfo(req: Request, db: Session = Depends(get_db)):
    try:
        if 'logined_uid' not in req.session:  # 로그인하지 않았다면
            return RedirectResponse(url='/member/login', status_code=303)

        # 로그인 했다면 아이디로 회원정보 조회 후 myinfo에 출력
        myinfo = MemberService.selectone_member(db, req.session['logined_uid'])
        print('--> ', myinfo)
        return templates.TemplateResponse('member/myinfo.html', {'request': req, 'myinfo': myinfo})

    except Exception as ex:
        print(f'▷▷▷ myinfo 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


@member_router.get('/error', response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('member/error.html', {'request': req})


@member_router.get('/loginfail', response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('member/loginfail.html', {'request': req})



# 엔드포인트 설정


