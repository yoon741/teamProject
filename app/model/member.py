from sqlalchemy import String, Integer, Date, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from app.model.base import Base
from datetime import datetime, date


class Member(Base):
    __tablename__ = 'member'

    mno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    userid: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(15))  # 전화번호를 문자열로 처리
    address: Mapped[str] = mapped_column(String(255))
    postcode: Mapped[str] = mapped_column(String(20))
    birthdate: Mapped[date] = mapped_column(Date)  # 생년월일을 Date 타입으로 처리
    gender: Mapped[str] = mapped_column(String(10))
    regdate: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # 등록일 기본값을 데이터베이스 함수로 설정
