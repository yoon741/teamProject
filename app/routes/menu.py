from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

menu_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@menu_router.get("/company", response_class=HTMLResponse)
async def company(request: Request):
    return templates.TemplateResponse("menu/company.html", {"request": request})

@menu_router.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("menu/welcome.html", {"request": request})

