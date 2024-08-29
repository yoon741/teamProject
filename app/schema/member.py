from pydantic import BaseModel, EmailStr, Field, constr
from datetime import date

class NewMember(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    userid: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    password: constr(min_length=6, max_length=100)
    phone: constr(max_length=15, pattern=r'^\d{10,15}$')
    address: str = Field(..., max_length=100)
    postcode: str = Field(..., max_length=10)
    birthdate: date
    gender: constr(pattern='^(male|female|other)$')

    class Config:
        arbitrary_types_allowed = True
