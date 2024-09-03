from sqlalchemy.orm import Session
from fastapi import HTTPException
import os
from datetime import datetime
from fastapi import Form
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from app.model.product import Product, PrdAttach
from app.schema.product import NewProduct

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/html/cdn/img/'

class ProductService:
    @staticmethod
    def get_all_products(db: Session):
        try:
            products = db.query(Product).all()
            return products
        except Exception as ex:
            print(f'Get All Products Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to retrieve products")

    @staticmethod
    def get_product_detail(db: Session, prdno: int):
        try:
            product = db.query(Product).filter(Product.prdno == prdno).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
        except Exception as ex:
            print(f'Get Product Detail Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to retrieve product detail")

    @staticmethod
    def update_product_qty(db: Session, prdno: int, qty: int):
        try:
            product = db.query(Product).filter(Product.prdno == prdno).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product.qty -= qty
            db.commit()
            return product
        except Exception as ex:
            db.rollback()
            print(f'Update Product Quantity Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Failed to update product quantity")

    @staticmethod
    def get_product_data(prdname: str = Form(...),
                         price: int = Form(...), type: str = Form(...),
                         qty: int = Form(...), description: str = Form(...)):
        return NewProduct(prdname=prdname, price=price, type=type, qty=qty, description=description)

    @staticmethod
    async def process_upload(files):
        attachs = []  # 업로드된 파일정보를 저장하기 위해 리스트 생성

        today = datetime.today().strftime('%Y%m%d%H%M') # UUID 생성
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

    @staticmethod
    def insert_product(prd, attachs, db):
        try:
            stmt = insert(Product).values(prdname=prd.prdname, price=prd.price, type=prd.type,
                                          qty=prd.qty, description=prd.description)
            result = db.execute(stmt)

            # 방금 insert된 레코드의 기본키 값 : inserted_primary_key
            inserted_prdno = result.inserted_primary_key[0]
            for attach in attachs:
                data = {'fname': attach[0], 'fsize': attach[1], 'prdno': inserted_prdno}
                stmt = insert(PrdAttach).values(data)
                result = db.execute(stmt)

            db.commit()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_gallery에서 오류발생 : {str(ex)} ')
            db.rollback()
