from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BoardBase(BaseModel):
    title: str
    userid: str
    contents: str

class BoardCreate(BoardBase):
    pass

class BoardRead(BoardBase):
    bno: int
    regdate: Optional[datetime]
    views: int

