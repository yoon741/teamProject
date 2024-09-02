from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import Base
from datetime import datetime

class Member(Base):
    __tablename__ = 'member'

    mno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    userid: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(15))
    address: Mapped[str] = mapped_column(String(255))
    postcode: Mapped[str] = mapped_column(String(20))
    birthdate: Mapped[Date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(10))
    regdate: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    orders = relationship("Order", back_populates="member")
    carts = relationship("Cart", back_populates="member")
