from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    userid: str = 'ubuntu'
    passwd: str = 'ubuntu'
    dbname: str = 'clouds2024'
    dburl: str = 'localhost'
    #dbconn: str = f'sqlite:///app/{dbname}.db'
    #?charset=utf8mb4 이모지 추가기능
    dbconn: str = f'mysql+pymysql://{userid}:{passwd}@{dburl}:3306/{dbname}?charset=utf8mb4'

config = Settings()
