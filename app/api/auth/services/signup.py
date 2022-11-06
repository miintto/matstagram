from sqlalchemy.orm import Session

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.jwt import JWTHandler
from app.common.types import ResultDict
from ..schemas import SignUpBody


class SignUp:
    @staticmethod
    def _validate(body: SignUpBody, session: Session):
        if body.password != body.password_check:
            raise APIException(Http4XX.BAD_REQUEST, data="비밀번호가 서로 일치하지 않습니다.")
        if session.query(AuthUser).filter(
            AuthUser.user_email == body.user_email
        ).first():
            raise APIException(
                Http4XX.DUPLICATED_USER_EMAIL, data=body.user_email
            )

    @staticmethod
    def _create_user(body: SignUpBody, session: Session) -> AuthUser:
        user = AuthUser(
            user_name=body.user_email,
            user_email=body.user_email,
            user_permission=UserPermission.normal,
        )
        user.set_password(body.password)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def _generate_token(user: AuthUser) -> dict:
        handler = JWTHandler()
        return {
            "access": handler.generate_access_token(user),
            "refresh": handler.generate_refresh_token(user),
        }

    def run(self, body: SignUpBody, session: Session) -> ResultDict:
        self._validate(body, session)
        user = self._create_user(body, session)
        return self._generate_token(user)
