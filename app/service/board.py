from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.board import Board
from app.schema.board import BoardCreate


class BoardService:
    @staticmethod
    def select_board(db, cpg):
        try:
            stbno = (cpg - 1) * 25
            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views) \
                .order_by(Board.bno.desc()) \
                .offset(stbno).limit(25)
            result = db.execute(stmt)

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_board 오류발생 : {str(ex)}')



@staticmethod
def create_board(db: Session, board: BoardCreate):
    new_board = Board(**board.dict())
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@staticmethod
def get_board(db: Session, bno: int):
    db_board = db.query(Board).filter(Board.bno == bno).first()
    if not db_board:
        from http.client import HTTPException
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

@staticmethod
def get_boards(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Board).offset(skip).limit(limit).all()