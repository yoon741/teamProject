from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from app.model.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'product'
    prdno = Column(Integer, primary_key=True, autoincrement=True)
    prdname = Column(String(100), nullable=False)
    price = Column(String(20), nullable=False)
    type = Column(String(50), nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    regdate = Column(DateTime, default=datetime.now, nullable=True)

class PrdAttach(Base):
    __tablename__ = 'prdattach'
    prdatno = Column(Integer, primary_key=True, autoincrement=True)
    prdno = Column(Integer, ForeignKey('product.prdno'))
    img1 = Column(String(50), nullable=False)
    img2 = Column(String(50), nullable=False)
    img3 = Column(String(50), nullable=False)
    img4 = Column(String(50), nullable=False)
