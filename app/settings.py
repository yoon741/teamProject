from pydantic.v1 import BaseSettings  # Pydantic의 BaseSettings를 임포트합니다. (Pydantic의 v1 버전 사용)

class Settings(BaseSettings):
    userid: str = ''        # 사용자 ID를 나타내는 설정값입니다. 기본값은 빈 문자열입니다.
    passwd: str = ''        # 비밀번호를 나타내는 설정값입니다. 기본값은 빈 문자열입니다.
    dbname: str = 'cloud2024'  # 데이터베이스 이름을 나타내는 설정값입니다. 기본값은 'cloud2024'입니다.
    dburl: str = f''       # 데이터베이스 URL을 나타내는 설정값입니다. 기본값은 빈 문자열입니다.
    dbconn: str = f'sqlite:///{dbname}.db'  # 데이터베이스 연결 문자열을 나타내는 설정값입니다.
    # 기본값은 `sqlite:///cloud2024.db`입니다. `dbname`이 'cloud2024'로 설정되어 있으므로,
    # `dbconn`은 `sqlite:///cloud2024.db`로 설정됩니다.
# Settings 클래스의 인스턴스를 생성합니다. 이 인스턴스는 설정값을 읽고 제공합니다.
config = Settings()
