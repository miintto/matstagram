from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSignUp:
    def _request_signup(self, payload, status_code):
        response = client.post("/api/auth/signup", json=payload)
        assert response.status_code == status_code
        return response.json()

    def test_signup_success(self):
        """회원가입 성공 케이스"""
        request_body = {
            "user_email": "test@test.com",
            "password": "1234",
            "password_check": "1234",
        }
        self._request_signup(request_body, 201)

    def test_signup_duplicated_email(self):
        """회원가입 중복된 이메일"""
        request_body = {
            "user_email": "matstagram@test.com",
            "password": "1234",
            "password_check": "1234",
        }
        res = self._request_signup(request_body, 422)
        assert res.get("code") == "F008"

    def test_signup_password_not_matched(self):
        """회원가입 비밀번호 불일치"""
        request_body = {
            "user_email": "test@test.com",
            "password": "1234",
            "password_check": "123456",
        }
        res = self._request_signup(request_body, 422)
        assert res.get("code") == "F000"

    def test_signup_password_invalid_email(self):
        """회원가입 이메일 형식 에러"""
        request_body = {
            "user_email": "test",
            "password": "1234",
            "password_check": "1234",
        }
        res = self._request_signup(request_body, 422)
        assert res.get("code") == "F000"
