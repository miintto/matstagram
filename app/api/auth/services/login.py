from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.jwt import JWTHandler
from app.common.types import ResultDict
from ..schemas import LogInBody


class LogIn:
    @staticmethod
    def _get_user(user_email: str, session: Session) -> AuthUser:
        try:
            user = session.query(AuthUser).filter(
                AuthUser.user_email == user_email, AuthUser.is_active
            ).one()
        except NoResultFound:
            raise APIException(Http4XX.USER_NOT_FOUND)
        return user

    @staticmethod
    def _generate_token(user: AuthUser) -> dict:
        handler = JWTHandler()
        return {
            "access": handler.generate_access_token(user),
            "refresh": handler.generate_refresh_token(user),
        }

    def run(self, body: LogInBody, session: Session) -> ResultDict:
        user = self._get_user(body.user_email, session)
        if not user.check_password(body.password):
            raise APIException(Http4XX.INVALID_PASSWORD)
        return self._generate_token(user)
