from app.api.auth.schemas import TokenResponse
from app.common.schemas import CommonResponse
from tests.management.fixtures import PyTestFixtures
from tests.management.testcase import BaseTestCase


class TestSignUp(BaseTestCase, PyTestFixtures):
    """회원가입 테스트"""

    def _request_signup(self, body, status_code, model=CommonResponse):
        response = self.client.post("/api/auth/signup", json=body)
        assert response.status_code == status_code
        return model(**response.json())

    def test_signup_success(self):
        """회원가입 성공 케이스"""
        self._request_signup(
            body={
                "user_email": "test@test.com",
                "password": "1234",
                "password_check": "1234",
            },
            status_code=200,
            model=TokenResponse,
        )

    def test_signup_duplicated_email(self, create_root_user):
        """회원가입 중복된 이메일"""
        response = self._request_signup(
            body={
                "user_email": "matstagram@test.com",
                "password": "1234",
                "password_check": "1234",
            },
            status_code=422,
        )
        assert response.code == "F008"

    def test_signup_password_not_matched(self):
        """회원가입 비밀번호 불일치"""
        response = self._request_signup(
            body={
                "user_email": "test@test.com",
                "password": "1234",
                "password_check": "123456",
            },
            status_code=422,
        )
        assert response.code == "F009"

    def test_signup_password_invalid_email(self):
        """회원가입 이메일 형식 에러"""
        response = self._request_signup(
            body={
                "user_email": "test",
                "password": "1234",
                "password_check": "1234",
            },
            status_code=400,
        )
        assert response.code == "F000"
