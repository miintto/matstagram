from app.api.user.models import AuthUser, UserPermission
from app.common.security.jwt import JWTHandler
from tests.management.fixtures import PyTestFixtures
from tests.management.testcase import BaseTestCase


class TestClint(BaseTestCase, PyTestFixtures):
    """웹 프론트 화면 테스트"""

    def test_client_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_client_map(self):
        response = self.client.get("/map")
        assert response.status_code == 200

    def test_client_register(self):
        response = self.client.get("/register")
        assert response.status_code == 200

    def test_client_documents(self, session):
        user = AuthUser(user_name="master", user_email="master@test.com", user_permission=UserPermission.admin)
        session.add(user)
        session.commit()

        response = self.client.get("/documents")
        assert response.status_code == 200

        token = JWTHandler().generate_access_token(user)
        response = self.client.get("/documents", cookies={"access": token})
        assert response.status_code == 200
