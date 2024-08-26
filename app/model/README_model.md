# /app/model 디렉토리
+ 컬럼 포함 테이블 모델 만드는 곳
+ __init__.py # 디렉토리 python 화
+ /base.py   # 베이스 모델
+ /member.py # class Member(Base): __tablename__ = 'member'
+ /cart.py   # class Cart(Base):__tablename__ = 'cart'
+ /board.py  # class Board(Base):__tablename__ = 'board'
+ /order.py  # class Order(Base):__tablename__ = 'order'
+ /product.py #class Product(Base):__tablename__ = 'product'