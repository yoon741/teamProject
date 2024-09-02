from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.product import Product

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
