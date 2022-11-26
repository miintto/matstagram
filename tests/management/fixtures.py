import pytest

from app.api.user.models import AuthUser


class PyTestFixtures:
    fixture_root_email = "matstagram@test.com"
    fixture_root_password = "1234"

    @pytest.fixture()
    def session(self):
        session = self.db._session()
        try:
            yield session
        finally:
            session.close()

    @pytest.fixture()
    def create_root_user(self, session):
        response = self.client.post(
            url="/api/auth/signup",
            json={
                "user_email": self.fixture_root_email,
                "password": self.fixture_root_password,
                "password_check": self.fixture_root_password,
            },
        )
        assert response.status_code == 200
        yield response.json()
        session.query(AuthUser).filter(
            AuthUser.user_email == self.fixture_root_email
        ).delete()
        session.commit()
