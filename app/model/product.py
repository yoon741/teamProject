from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'product'
    prdno = Column(Integer, primary_key=True, autoincrement=True)
    prdname = Column(String(100), nullable=False)
    price = Column(String(20), nullable=False)
    type = Column(String(50), nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    description = Column(String(100))
    regdate = Column(DateTime, default=datetime.now, nullable=True)

    carts = relationship("Cart", back_populates="product")


class PrdAttach(Base):
    __tablename__ = 'prdattach'
    prdatno = Column(Integer, primary_key=True, autoincrement=True)
    prdno = Column(Integer, ForeignKey('product.prdno'))
    img1 = Column(String(50), nullable=False)
    img2 = Column(String(50), nullable=False)
    img3 = Column(String(50), nullable=False)
    img4 = Column(String(50), nullable=False)

class Cart(Base):
    __tablename__ = 'cart'
    cno = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer, ForeignKey('member.mno'), nullable=False)
    prdno = Column(Integer, ForeignKey('product.prdno'), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="carts")