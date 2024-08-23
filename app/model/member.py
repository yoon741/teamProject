from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped

from app.model.base import Base


class Member(Base):
    __tablename__ = 'member'

    mno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)  # 식별관계
    # userid: Mapped[str] = mapped_column(index=True)  # 비식별관계
    passwd: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)

# 테이블 매핑