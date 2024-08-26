# 수업 맴버 스키마
from pydantic import BaseModel

class NewMember(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    captcha: str

# 유효성 검사

from pydantic import BaseModel, EmailStr
from datetime import datetime

class MemberCreate(BaseModel):
    userid: str
    passwd: str
    name: str
    email: EmailStr
    addr: str = None
    birth: str = None
    phone: str = None

class MemberRead(BaseModel):
    mno: int
    userid: str
    name: str
    email: str
    addr: str = None
    birth: str = None
    phone: str = None
    point: int
    regdate: datetime

