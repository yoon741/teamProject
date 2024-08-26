from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.product import Product
from app.schema.product import ProductRead
from app.dbfactory import get_db

shop_router = APIRouter()

# shop 라우터 제품번호에 따른 엔드포인트 지정
# 관리자입장 / 회원입장 라우트 된 엔드포인트가 달라야 한다

# ex)
# member/product/{prdno}
# admin/product/{prdno}
@shop_router.get("/product/{prdno}", response_model=ProductRead)
def read_product(prdno: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.prdno == prdno).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
