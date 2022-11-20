import pytest

from app.api.user.models import AuthUser


class PyTestFixtures:
    @pytest.fixture()
    def session(self):
        session = self.db._session()
        try:
            yield session
        finally:
            session.close()

    @pytest.fixture()
    def create_root_user(self, session):
        user_email = "matstagram@test.com"
        response = self.client.post(
            url="/api/auth/signup",
            json={
                "user_email": user_email,
                "password": "1234",
                "password_check": "1234",
            },
        )
        assert response.status_code == 200
        yield response.json()
        session.query(AuthUser).filter(
            AuthUser.user_email == user_email
        ).delete()
        session.commit()
