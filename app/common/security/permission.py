from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import APIException
from app.common.http.codes import Http4XX
from app.config.connection import db
from app.domain.models.user import AuthUser, UserPermission
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

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
        session: AsyncSession = Depends(db.session),
    ) -> AuthUser | None:
        return await self.authorization(credentials, session)

    async def get_user(
        self, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> AuthUser:
        try:
            result = await session.execute(
                select(AuthUser).where(AuthUser.id == credentials.payload.pk)
            )
            return result.scalar_one()
        except NoResultFound:
            raise APIException(Http4XX.PERMISSION_DENIED)

    async def authorization(self, *args, **kwargs):
        raise NotImplementedError


class IsAuthenticated(BasePermission):
    async def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> AuthUser:
        return await self.get_user(credentials, session)


class IsNormalUser(BasePermission):
    async def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> AuthUser:
        user = await self.get_user(credentials, session)
        if user.user_permission not in (
            UserPermission.NORMAL, UserPermission.ADMIN
        ):
            raise APIException(Http4XX.PERMISSION_DENIED)
        return user


class AdminOnly(BasePermission):
    async def authorization(
        self, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> AuthUser:
        user = await self.get_user(credentials, session)
        if not user.user_permission.is_admin():
            raise APIException(Http4XX.PERMISSION_DENIED)
        return user
