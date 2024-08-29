import hashlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model.member import Member
from app.schema.member import NewMember

class MemberService:
    @staticmethod
    def sha256_hash(passwd: str) -> str:
        """
        SHA-256 암호화 함수
        """
        hash_object = hashlib.sha256()
        hash_object.update(passwd.encode('utf-8'))
        return hash_object.hexdigest()
    @staticmethod
    def insert_member(db: Session, member: NewMember):
        try:
            hashed_password = MemberService.sha256_hash(member.password)
            stmt = Member(
                username=member.username,
                userid=member.userid,
                email=member.email,
                password=hashed_password,
                phone=member.phone,
                address=member.address,
                postcode=member.postcode,
                birthdate=member.birthdate,
                gender=member.gender
            )
            db.add(stmt)
            db.commit()
            db.refresh(stmt)  # 데이터베이스에서 새로 삽입된 데이터 새로 고침
            print(f"Inserted member: {stmt}")
            return stmt
        except SQLAlchemyError as ex:
            db.rollback()
            print(f'Insert Member Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def login_member(db: Session, data: dict):
        try:
            hashed_password = MemberService.sha256_hash(data['password'])
            member = db.query(Member).filter(
                Member.userid == data['userid'],
                Member.password == hashed_password
            ).first()
            return member
        except SQLAlchemyError as ex:
            print(f'Login Error: {str(ex)}')
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def is_userid_taken(db: Session, userid: str) -> bool:
        existing_user = db.query(Member).filter(Member.userid == userid).first()
        return existing_user is not None
