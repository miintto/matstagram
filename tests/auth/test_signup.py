import pytest
from sqlalchemy import select

from app.api.auth.schemas import TokenResponse
from app.common.schemas import CommonResponse
from app.domain.models.user import AuthUser
from tests.conftest import fixture_root_email
from tests.management.testcase import BaseTestCase


class TestSignUp(BaseTestCase):
    """회원가입 테스트"""

    async def _request_signup(self, body, status_code, model=CommonResponse):
        response = await self.client.post("/api/auth/signup", json=body)
        assert response.status_code == status_code
        return model(**response.json())

    @pytest.mark.asyncio
    async def test_signup_success(self, session):
        """회원가입 성공 케이스"""
        user_email = "test@test.com"
        await self._request_signup(
            body={
                "user_email": user_email,
                "password": "1234",
                "password_check": "1234",
            },
            status_code=200,
            model=TokenResponse,
        )
        result = await session.execute(
            select(AuthUser).where(AuthUser.user_email == user_email)
        )
        assert result.scalar_one()

    @pytest.mark.asyncio
    async def test_signup_duplicated_email(self, create_root_user):
        """회원가입 중복된 이메일"""
        response = await self._request_signup(
            body={
                "user_email": fixture_root_email,
                "password": "1234",
                "password_check": "1234",
            },
            status_code=422,
        )
        assert response.code == "F008"

    @pytest.mark.asyncio
    async def test_signup_password_not_matched(self):
        """회원가입 비밀번호 불일치"""
        response = await self._request_signup(
            body={
                "user_email": "test2@test.com",
                "password": "1234",
                "password_check": "123456",
            },
            status_code=422,
        )
        assert response.code == "F009"

    @pytest.mark.asyncio
    async def test_signup_password_invalid_email(self):
        """회원가입 이메일 형식 에러"""
        response = await self._request_signup(
            body={
                "user_email": "test",
                "password": "1234",
                "password_check": "1234",
            },
            status_code=400,
        )
        assert response.code == "F000"
