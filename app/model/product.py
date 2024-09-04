from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import Base
from datetime import datetime


class Product(Base):
    __tablename__ = 'product'

    prdno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prdname = Column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column (String(50), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[int] = mapped_column(String(250))
    regdate: Mapped[int] = mapped_column(default=datetime.now, nullable=True)

    carts = relationship("Cart", back_populates="product")
    orders = relationship("Order", back_populates="product")
    attachs = relationship("PrdAttach", back_populates="product")

class PrdAttach(Base):
    __tablename__ = 'prdattach'

    prdatno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prdno: Mapped[int] = mapped_column(Integer, ForeignKey('product.prdno'))
    fname: Mapped[str] = mapped_column(String(50), nullable=False)
    fsize: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product", back_populates="attachs")


class Cart(Base):
    __tablename__ = 'cart'
    cno = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer, ForeignKey('member.mno'), nullable=False)
    prdno = Column(Integer, ForeignKey('product.prdno'), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    member = relationship('Member', back_populates='carts')
    product = relationship('Product', back_populates='carts')
