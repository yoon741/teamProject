from pydantic import BaseModel

class NewMember(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    captcha: str

# 유효성 검사