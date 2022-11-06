from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestLogIn:
    def _request_signup(self, payload, status_code):
        response = client.post("/api/auth/login", json=payload)
        assert response.status_code == status_code
        return response.json()

    def test_login_success(self):
        """회원가입 성공 케이스"""
        request_body = {
            "user_email": "matstagram@test.com",
            "password": "1234",
        }
        self._request_signup(request_body, 200)

    def test_login_invalid_email(self):
        """회원가입 이메일 불일치"""
        request_body = {
            "user_email": "matstagram@test.net",
            "password": "1234",
        }
        res = self._request_signup(request_body, 404)
        assert res.get("code") == "F003"

    def test_login_invalid_password(self):
        """회원가입 비밀번호 불일치"""
        request_body = {
            "user_email": "matstagram@test.com",
            "password": "12341234",
        }
        res = self._request_signup(request_body, 422)
        assert res.get("code") == "F004"
