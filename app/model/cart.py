from sqlalchemy import Column, Integer, String
from app.model.base import Base

class Cart(Base):
    __tablename__ = 'cart'
    cno = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer, nullable=False)
    prdno = Column(Integer, nullable=False)
    size = Column(String(20), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
