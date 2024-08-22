import requests
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.model.member import Member

class MemberService:
    @staticmethod
    def insert_member(db, member):
        try:
            # 정상적 실행 구간
            stmt = insert(Member).values(
                userid=member.userid, passwd=member.passwd,
                name=member.name, email=member.email)
            result = db.execute(stmt)
            db.flush()
            db.commit()
            return result

        except SQLAlchemyError as ex:
            # 오류발생 시 실행 구간
            print(f'▶▶▶ insert_member 오류발생: {str(ex)}')
            db.rollback()

    # google recaptcha 확인 url
    # 비밀키 쓰는곳
    # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(member):
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        # 구글 캡챠 비밀키 넣는 곳 - 퍼블릭에 커밋하지 말기!!
        params = { 'secret': '',
                   'response': member.captcha }
        res = requests.get(req_url, params=params)
        result = res.json()
        print('check=> ', result)

        return result['success']
        return True

    @staticmethod
    def login_member(db, data):
        try:
            find_login = and_(Member.userid == data.get('userid'),
                              Member.userid == data.get('passwd'))
            stmt = select(Member.userid).where(find_login)
            result = db.execute(stmt).scalars().first()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ login_member 오류발생 :  {str(ex)}')

    @staticmethod
    def selectone_member(db, userid):
        try:
            find_uid = Member.userid == userid
            stmt = select(Member).where(find_uid)
            result = db.execute(stmt).scalars()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_member 오류 발생 : {str(ex)}')


# memberCRUD
# - 인서트 구현
# - 로그인 리딩 구현
