# /app 디렉토리
+ DB 설정하는곳
  + dbfactory.py
    + DB의 세션 관리
  + settings.py
    + DB 인스턴스 생성
  + base로 시작
  + async def db_startup():
    from app import settings
    print(f"Database connection string: {settings.db_conn}")
    Base.metadata.create_all(bind=engine)