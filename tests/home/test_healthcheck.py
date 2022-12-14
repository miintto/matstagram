from tests.management.testcase import BaseTestCase


class TestHealthCheck(BaseTestCase):
    def test_healthcheck(self):
        response = self.client.get("/healthcheck")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json.get("status") == "ok"
        assert res_json.get("version") is not None
