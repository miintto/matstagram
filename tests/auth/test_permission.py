import pytest
from sqlalchemy import delete

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.permission import (
    AdminOnly,
    IsAuthenticated,
    IsNormalUser,
)
from app.common.security.schemas import HTTPAuthorizationCredentials
from app.common.security.jwt import JWTHandler
from tests.management.testcase import BaseTestCase


class TestPermission(BaseTestCase):
    """권한 관리 모듈 테스트"""

    def _generate_credentials(self, user):
        token = JWTHandler().generate_access_token(user)
        return HTTPAuthorizationCredentials(
            scheme="JWT",
            token=token,
            payload=JWTHandler().decode_token(token)
        )

    @pytest.mark.asyncio
    async def test_permission_normal(self, session):
        user = AuthUser(
            user_name="test-user",
            user_email="test@test.com",
            user_permission=UserPermission.NORMAL,
        )
        session.add(user)
        await session.flush()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        await permission(credentials=credentials, session=session)

        permission = IsNormalUser()
        await permission(credentials=credentials, session=session)

        with pytest.raises(APIException) as e:
            permission = AdminOnly()
            await permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

    @pytest.mark.asyncio
    async def test_permission_anonymous(self, session):
        user = AuthUser(
            user_name="ANONYMOUS",
            user_email="ANONYMOUS",
            user_permission=UserPermission.ANONYMOUS,
        )
        session.add(user)
        await session.flush()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        await permission(credentials=credentials, session=session)

        with pytest.raises(APIException) as e:
            permission = IsNormalUser()
            await permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

        with pytest.raises(APIException) as e:
            permission = AdminOnly()
            await permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

    @pytest.mark.asyncio
    async def test_permission_admin(self, session):
        user = AuthUser(
            user_name="master",
            user_email="admin@test.com",
            user_permission=UserPermission.ADMIN,
        )
        session.add(user)
        await session.flush()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        await permission(credentials=credentials, session=session)

        permission = IsNormalUser()
        await permission(credentials=credentials, session=session)

        permission = AdminOnly()
        await permission(credentials=credentials, session=session)

    @pytest.mark.asyncio
    async def test_permission_user_not_existed(self, session):
        user = AuthUser(
            user_name="null",
            user_email="not-exist@test.com",
            user_permission=UserPermission.NORMAL
        )
        session.add(user)
        await session.flush()
        credentials = self._generate_credentials(user)
        await session.execute(
            delete(AuthUser).where(AuthUser.user_name == "null")
        )

        with pytest.raises(APIException) as e:
            permission = IsAuthenticated()
            await permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED
