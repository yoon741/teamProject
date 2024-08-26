
from sqlalchemy import Column, Integer, String, DateTime
from app.model.base import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'
    omno = Column(Integer, primary_key=True, autoincrement=True)
    mno = Column(Integer,nullable=False)
    prdno = Column(Integer, nullable=False)
    size = Column(String(50), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    postcode = Column(String(10), nullable=False)
    addr = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    regdate = Column(DateTime, default=datetime.now(), nullable=True)
