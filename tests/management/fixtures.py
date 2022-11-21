import pytest

from app.api.user.models import AuthUser
from app.main import app


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

    @pytest.fixture()
    def exclude_middleware(self):
        """router의 결과로 TemplateResponse 를 반환하는 경우 starlette middleware 에서
        에러가 발생하므로 임시로 middleware 를 제거 후 테스트 하였습니다."""
        _user_middleware = app.user_middleware.copy()
        app.user_middleware = []
        app.middleware_stack = app.build_middleware_stack()
        yield
        app.user_middleware = _user_middleware
        app.middleware_stack = app.build_middleware_stack()
