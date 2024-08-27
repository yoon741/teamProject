from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.dbfactory import db_startup, db_shutdown
from app.routes.admin import admin_router
from app.routes.board import board_router
from app.routes.cart import cart_router
from app.routes.gallery import gallery_router
from app.routes.main_header import main_header_router
from app.routes.member import member_router
from app.routes.menu import menu_router
from app.routes.menu_footer import footer_router
from app.routes.order import order_router
from app.routes.shop import shop_router
from app.routes.side_header import side_header_router


# from app.routes.menu_footer import footer_router
# from app.routes.main_header import main_header_router
# from app.routes.side_header import side_header_router
# from app.routes.order import order_router
# from app.routes.shop import shop_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_startup()
    yield
    await db_shutdown()


app = FastAPI(lifespan=lifespan)

# 세션처리를 위해 미들웨어 설정
# pip install itsdangerous
app.add_middleware(SessionMiddleware, secret_key='20240822110005')

templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'),name='static')

app.include_router(member_router, prefix='/member')
app.include_router(board_router, prefix='/board')
app.include_router(menu_router, prefix="/menu")
app.include_router(main_header_router, prefix='/menu/headermain')
app.include_router(side_header_router, prefix='/menu/headerside')
app.include_router(footer_router, prefix='/menu/footer')
app.include_router(shop_router, prefix='/shop')
app.include_router(order_router, prefix='/order')
app.include_router(cart_router, prefix='/cart')
app.include_router(gallery_router, prefix='/gallery')
app.include_router(admin_router, prefix='/admin')

@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)