from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSignUp:
    def test_healthcheck(self):
        response = client.get("/healthcheck")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json.get("status") == "ok"
        assert res_json.get("version") is not None
