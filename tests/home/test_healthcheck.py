import pytest

from tests.management.testcase import BaseTestCase


class TestHealthCheck(BaseTestCase):
    @pytest.mark.asyncio
    async def test_healthcheck(self):
        response = await self.client.get("/healthcheck")
        assert response.status_code == 200
        assert eval(response.text) == "ok"

    @pytest.mark.asyncio
    async def test_status(self):
        response = await self.client.get("/status")
        assert response.status_code == 200
        res_json = response.json()
        assert res_json.get("status") == "ok"
        assert res_json.get("postgres") == "ok"
        assert res_json.get("redis") == "ok"
