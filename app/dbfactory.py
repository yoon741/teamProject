#기존 dbfactory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.base import Base

from app.model import member, board, gallery, cart, order, product
from app.settings import config

engine = create_engine(config.dbconn, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def db_startup():

    # Base.metadata.create_all(bind=engine)
    member.Base.metadata.create_all(engine)
    board.Base.metadata.create_all(engine)
    cart.Base.metadata.create_all(engine)
    order.Base.metadata.create_all(engine)
    product.Base.metadata.create_all(engine)
    gallery.Base.metadata.create_all(engine)

async def db_shutdown():
    pass
