from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import member  # 데이터베이스 모델을 가져옵니다
from app.settings import config  # 설정 파일에서 데이터베이스 연결 문자열을 가져옵니다

# SQLAlchemy 엔진을 생성합니다.
# `config.dbconn`은 데이터베이스 연결 문자열을 포함하고 있으며, `echo=True`는 SQL 쿼리를 로그에 출력하도록 설정합니다.
engine = create_engine(config.dbconn, echo=True)

# 세션 로컬을 설정합니다.
# `autocommit=False`는 자동 커밋 모드를 비활성화하며,
# `autoflush=False`는 자동 플러시 모드를 비활성화합니다.
# `bind=engine`는 이 세션이 위에서 생성한 엔진을 사용할 것임을 의미합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 생성자 함수입니다.
    이 함수는 SQLAlchemy의 의존성 주입 시스템에서 사용할 수 있습니다.
    """
    db = SessionLocal()  # 새로운 세션을 생성합니다
    try:
        yield db  # 세션을 반환하고, 호출된 곳에서 사용할 수 있도록 합니다.
    finally:
        db.close()  # 사용이 끝난 후 세션을 닫습니다.

async def db_startup():
    """
    애플리케이션 시작 시 데이터베이스를 초기화하는 함수입니다.
    데이터베이스에 정의된 모든 테이블을 생성합니다.
    """
    member.Base.metadata.create_all(engine)  # `member.Base`에서 정의된 모든 테이블을 생성합니다.

async def db_shutdown():
    """
    애플리케이션 종료 시 데이터베이스 자원을 정리하는 함수입니다.
    현재는 아무 작업도 수행하지 않지만, 필요에 따라 확장할 수 있습니다.
    """
    pass


# 데이터베이스 연결 및 세션 관리, 데이터베이스 초기화 기능을 제공하는 코드