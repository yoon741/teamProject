from typing import List

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.gallery import NewGallery
from app.service.galleryservice import get_gallery_data, process_upload, GalleryService

gallery_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@gallery_router.get('/list/{cpg}', response_class=HTMLResponse)
async def list(req: Request, db: Session = Depends(get_db)):
    try:
        return templates.TemplateResponse('gallery/list.html', {'request': req})

    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


@gallery_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    return templates.TemplateResponse('gallery/write.html', {'request': req})


@gallery_router.post('/write', response_class=HTMLResponse)
async def writeok(req: Request, gallery: NewGallery = Depends(get_gallery_data),
                  files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        print(gallery)
        attachs = await process_upload(files)
        print(attachs)
        if GalleryService.insert_gallery(gallery, attachs, db):
            return RedirectResponse('/gallery/list/1', 303)

    except Exception as ex:
        print(f'▷▷▷ writeok 오류발생 {str(ex)}')
        return RedirectResponse('/member/error', 303)


@gallery_router.get('/view', response_class=HTMLResponse)
async def view(req: Request):
    return templates.TemplateResponse('gallery/view.html', {'request': req})