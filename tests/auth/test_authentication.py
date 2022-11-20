from unittest.mock import Mock

import pytest

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.authentication import Authentication
from app.common.security.jwt import JWTHandler
from app.common.security.schemas import TokenType
from ..testcase import BaseTestCase


class TestAuthentication(BaseTestCase):
    """인증 모듈 테스트"""

    def _generate_token(self, user: AuthUser):
        return JWTHandler().generate_access_token(user)

    def _generate_fake_token(self, user):
        handler = JWTHandler()
        return handler._encode_token(
            exp_interval=handler.JWT_ACCESS_EXPIRATION_INTERVAL,
            type=TokenType.REFRESH.value,
            pk=user.id,
            permission=user.user_permission.name,
            user_name=user.user_name,
        )

    @pytest.mark.asyncio
    async def test_auth_success(self):
        user = AuthUser(
            id=1, user_name="test-user", user_permission=UserPermission.normal
        )
        token = self._generate_token(user)
        request = Mock(headers={"Authorization": f"JWT {token}"})

        auth_scheme = Authentication()
        credentials = await auth_scheme(request)
        assert credentials.scheme == "JWT"
        assert credentials.payload.type == TokenType.ACCESS

    @pytest.mark.asyncio
    async def test_auth_invalid_token(self):
        user = AuthUser(
            id=1, user_name="test-user", user_permission=UserPermission.normal
        )

        request = Mock(headers={})
        auth_scheme = Authentication()
        with pytest.raises(APIException) as e:
            await auth_scheme(request)
        assert e.value.error == Http4XX.UNAUTHENTICATED

        for token in [
            "JWT abcd1234",
            self._generate_token(user),
            f"Bearer {self._generate_token(user)}",
            f"JWT {JWTHandler().generate_refresh_token(user)}",
            f"JWT {self._generate_fake_token(user)}"
        ]:
            request.headers = {"Authorization": token}
            with pytest.raises(APIException) as e:
                await auth_scheme(request)
            assert e.value.error == Http4XX.UNAUTHENTICATED
