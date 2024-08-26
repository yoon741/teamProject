import os
from datetime import datetime

from fastapi import Form
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.model.gallery import Gallery, GalAttach
from app.schema.gallery import NewGallery

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/html/cdn/img/'

def get_gallery_data(title: str = Form(...),
                     userid: str = Form(...), contents: str = Form(...)):
    return NewGallery(userid=userid, title=title, contents=contents)

async def process_upload(files):
    attachs = []  # 업로드된 파일정보를 저장하기 위해 리스트 생성
    today = datetime.today().strftime('%Y%m%d%H%M%S') # UUID 생성
    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}{file.filename}'
            # os.path.join(A,B) => A/B (경로생성)
            fname = os.path.join(UPLOAD_PATH, nfname) # 업로드할 파일경로 생성
            content = await file.read()  # 업로드할 파일의 내용을 비동기로 읽음
            with open(fname, 'wb') as f:
                f.write(content)
            attach = [nfname, file.size] # 업로드된 파일 정보를 리스트에 저장
            attachs.append(attach)

    return attachs


class GalleryService:
    @staticmethod
    def insert_gallery(gal, attachs, db):
        try:
            stmt = insert(Gallery).values(userid=gal.userid,
                                          title=gal.title, contents=gal.contents)
            result = db.execute(stmt)

            # 방금 insert된 레코드의 기본키 값 : inserted_primary_key
            inserted_gno = result.inserted_primary_key[0]
            for attach in attachs:
                data = {'fname': attach[0], 'fsize': attach[1],
                        'gno': inserted_gno }
                stmt = insert(GalAttach).values(data)
                result = db.execute(stmt)

            db.commit()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_gallery에서 오류발생 : {str(ex)} ')
            db.rollback()