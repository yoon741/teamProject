from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from app.model.base import Base

class Member(Base):
    __tablename__ = 'member'  # 이 클래스가 매핑될 데이터베이스 테이블의 이름을 지정합니다.

    mno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(index=True)
    passwd: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)

# 테이블 매핑