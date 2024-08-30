from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.product import Product, PrdAttach
from app.schema.product import ProductCreate, PrdAttachCreate
class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        new_product = Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def get_product(db: Session, prdno: int):
        db_product = db.query(Product).filter(Product.prdno == prdno).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product

    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def create_prd_attach(db: Session, prd_attach: PrdAttachCreate):
        new_prd_attach = PrdAttach(**prd_attach.dict())
        db.add(new_prd_attach)
        db.commit()
        db.refresh(new_prd_attach)
        return new_prd_attach

    @staticmethod
    def get_prd_attach(db: Session, prdatno: int):
        db_prd_attach = db.query(PrdAttach).filter(PrdAttach.prdatno == prdatno).first()
        if not db_prd_attach:
            raise HTTPException(status_code=404, detail="Product attachment not found")
        return db_prd_attach

    @staticmethod
    def get_product_detail(db: Session, prdno: int):
        try:
            product = db.query(Product).filter(Product.prdno == prdno).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            return product
        except Exception as e:
            print(f"Failed to retrieve product detail: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to retrieve product detail")