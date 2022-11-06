from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.config.connection import db
from .authentication import Authentication, HTTPAuthorizationCredentials

auth_scheme = Authentication()


class BasePermission:
    """사용자의 접근 권한을 확인합니다.

    Args:
        credentials: 사용자 인증 세션
        session: sqlalchemy DB 세션 객체

    Examples:
        아래와 같이 해당 클래스를 상속받아 구체적인 검증 로직을 작성할 수 있습니다.

        ```python
        class DumpPermission(BasePermission):
            def authorization(self, credentials, session):
                ...
                return self.get_user(credentials, session)
        ```
    """

    def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
        session: Session = Depends(db.session),
    ) -> AuthUser | None:
        return self.authorization(credentials, session)

    def get_user(
        self, credentials: HTTPAuthorizationCredentials, session: Session
    ) -> AuthUser:
        try:
            return session.query(AuthUser).filter(
                AuthUser.id == credentials.payload.pk
            ).one()
        except NoResultFound:
            raise APIException(Http4XX.PERMISSION_DENIED)

    def authorization(self, *args, **kwargs):
        raise NotImplementedError


class IsAuthenticated(BasePermission):
    def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: Session
    ) -> AuthUser:
        return self.get_user(credentials, session)


class IsNormalUser(BasePermission):
    def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: Session
    ) -> AuthUser:
        user = self.get_user(credentials, session)
        if user.user_permission not in (
            UserPermission.normal, UserPermission.admin
        ):
            raise APIException(Http4XX.PERMISSION_DENIED)
        return user


class AdminOnly(BasePermission):
    def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: Session
    ) -> AuthUser:
        user = self.get_user(credentials, session)
        if not user.is_admin:
            raise APIException(Http4XX.PERMISSION_DENIED)
        return user
