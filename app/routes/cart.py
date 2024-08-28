from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model import cart
from app.schema.board import BoardCreate, BoardRead
from app.dbfactory import get_db

cart_router = APIRouter()



@cart_router.get("/cart/{cno}", response_model=BoardRead)
def read_board(cno: int, db: Session = Depends(get_db)):
    db_board = db.query(cart).filter(cart.cno == cno).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board
