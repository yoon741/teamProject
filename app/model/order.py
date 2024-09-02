from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.model.base import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'

    omno = Column(Integer, nullable=False)
    mno = Column(Integer, ForeignKey('member.mno'), nullable=False)
    prdno = Column(Integer, ForeignKey('product.prdno'), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    postcode = Column(String(10), nullable=False)
    addr = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    payment = Column(String(100), nullable=False)
    regdate = Column(DateTime, default=datetime.now, nullable=True)

    member = relationship("Member", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    __table_args__ = (
        PrimaryKeyConstraint('omno', 'prdno'),
    )