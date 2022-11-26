import pytest

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
from tests.management.fixtures import PyTestFixtures
from tests.management.testcase import BaseTestCase


class TestPermission(BaseTestCase, PyTestFixtures):
    """권한 관리 모듈 테스트"""

    def _generate_credentials(self, user):
        token = JWTHandler().generate_access_token(user)
        return HTTPAuthorizationCredentials(
            scheme="JWT",
            token=token,
            payload = JWTHandler().decode_token(token)
        )

    def test_permission_normal(self, session):
        user = AuthUser(
            user_name="test-user",
            user_email="test@test.com",
            user_permission=UserPermission.normal,
        )
        session.add(user)
        session.commit()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        permission(credentials=credentials, session=session)

        permission = IsNormalUser()
        permission(credentials=credentials, session=session)

        with pytest.raises(APIException) as e:
            permission = AdminOnly()
            permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

    def test_permission_anonymous(self, session):
        user = AuthUser(
            user_name="anonymous",
            user_email="anonymous",
            user_permission=UserPermission.anonymous,
        )
        session.add(user)
        session.commit()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        permission(credentials=credentials, session=session)

        with pytest.raises(APIException) as e:
            permission = IsNormalUser()
            permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

        with pytest.raises(APIException) as e:
            permission = AdminOnly()
            permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED

    def test_permission_admin(self, session):
        user = AuthUser(
            user_name="master",
            user_email="admin@test.com",
            user_permission=UserPermission.admin,
        )
        session.add(user)
        session.commit()
        credentials = self._generate_credentials(user)

        permission = IsAuthenticated()
        permission(credentials=credentials, session=session)

        permission = IsNormalUser()
        permission(credentials=credentials, session=session)

        permission = AdminOnly()
        permission(credentials=credentials, session=session)

    def test_permission_user_not_existed(self, session):
        user = AuthUser(
            user_name="null",
            user_email="not-exist@test.com",
            user_permission=UserPermission.normal
        )
        session.add(user)
        session.commit()
        credentials = self._generate_credentials(user)
        session.query(AuthUser).filter(AuthUser.user_name == "null").delete()

        with pytest.raises(APIException) as e:
            permission = IsAuthenticated()
            permission(credentials=credentials, session=session)
        assert e.value.error == Http4XX.PERMISSION_DENIED
