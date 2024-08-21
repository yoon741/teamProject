from datetime import datetime  # 날짜 및 시간 처리를 위해 datetime 모듈을 임포트합니다.
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy의 Mapped와 mapped_column을 임포트합니다.
from app.model.base import Base  # Base 클래스는 SQLAlchemy의 선언적 베이스 클래스로, 모델 클래스에서 상속받습니다.

class Member(Base):
    __tablename__ = 'member'  # 이 클래스가 매핑될 데이터베이스 테이블의 이름을 지정합니다.

    mno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    # mno 컬럼을 정의합니다:
    # - `primary_key=True`로 설정하여 기본 키로 지정합니다.
    # - `autoincrement=True`로 설정하여 자동으로 증가하도록 합니다.
    # - `index=True`로 설정하여 이 컬럼에 인덱스를 추가합니다.

    userid: Mapped[str] = mapped_column(index=True)
    # userid 컬럼을 정의합니다:
    # - `index=True`로 설정하여 이 컬럼에 인덱스를 추가합니다.

    passwd: Mapped[str]
    # passwd 컬럼을 정의합니다:
    # - 인덱스나 기본값 없이 문자열 타입으로 지정합니다.

    name: Mapped[str]
    # name 컬럼을 정의합니다:
    # - 문자열 타입으로 지정합니다.

    email: Mapped[str]
    # email 컬럼을 정의합니다:
    # - 문자열 타입으로 지정합니다.

    regdate: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    # regdate 컬럼



# 테이블 매핑