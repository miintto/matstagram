import pytest

from app.api.auth.schemas import TokenResponse
from app.common.schemas import CommonResponse
from tests.management.testcase import BaseTestCase


class TestLogIn(BaseTestCase):
    """로그인 테스트"""

    async def _request_login(self, body, status_code, model=CommonResponse):
        response = await self.client.post("/api/auth/login", json=body)
        assert response.status_code == status_code
        return model(**response.json())

    @pytest.mark.asyncio
    async def test_login_success(self, create_root_user):
        """로그인 성공 케이스"""
        await self._request_login(
            body={"user_email": "matstagram@test.com", "password": "1234"},
            status_code=200,
            model=TokenResponse
        )

    @pytest.mark.asyncio
    async def test_login_fail(self, create_root_user):
        """로그인 실패 케이스"""
        # 파라미터 에러
        response = await self._request_login(
            body={"user_email": "matstagram@test.comm"},
            status_code=400,
        )
        assert response.code == "F000"

        # 이메일 불일치
        response = await self._request_login(
            body={"user_email": "matstagram@test.comm", "password": "1234"},
            status_code=404,
        )
        assert response.code == "F003"

        # 비밀번호 불일치
        response = await self._request_login(
            body={"user_email": "matstagram@test.com", "password": "12341234"},
            status_code=422,
        )
        assert response.code == "F004"
