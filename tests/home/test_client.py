import pytest

from app.common.security.jwt import JWTHandler
from app.domain.models.user import AuthUser, UserPermission
from tests.management.testcase import BaseTestCase


class TestClint(BaseTestCase):
    """웹 프론트 화면 테스트"""

    @pytest.mark.asyncio
    async def test_client_home(self):
        response = await self.client.get("/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_client_map(self):
        response = await self.client.get("/map")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_client_register(self):
        response = await self.client.get("/register")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_client_documents(self, session):
        user = AuthUser(
            user_name="master",
            user_email="master@test.com",
            user_permission=UserPermission.ADMIN,
        )
        session.add(user)
        await session.flush()

        response = await self.client.get("/documents")
        assert response.status_code == 200

        token = JWTHandler().generate_access_token(user)
        response = await self.client.get("/documents", cookies={"access": token})
        assert response.status_code == 200
