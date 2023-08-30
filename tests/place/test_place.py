import pytest

from app.api.place.schemas.resopnse import (
    PlaceCreatedResponse,
    PlaceListResponse,
    PlaceResponse,
)
from app.common.schemas import CommonResponse
from tests.management.testcase import BaseTestCase


class TestPlace(BaseTestCase):
    """장소 테스트"""

    @pytest.mark.asyncio
    async def test_place_success(self, create_root_user):
        access = create_root_user["data"]["access"]
        # 장소 등록
        response = await self.client.post(
            "/api/place",
            json={
                "place_name": "장소1",
                "description": "첫번째 장소입니다.",
                "lat": 37.543,
                "lng": 127.123,
                "tag_ids": [],
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        PlaceCreatedResponse(**response.json())

        # description 없이도 등록 가능
        response = await self.client.post(
            "/api/place",
            json={
                "place_name": "장소2",
                "lat": 37.55,
                "lng": 126.9876,
                "tag_ids": [],
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        PlaceCreatedResponse(**response.json())

        # 장소 리스트 조회
        response = await self.client.get(
            "/api/place", headers={"Authorization": f"JWT {access}"}
        )
        assert response.status_code == 200
        result = PlaceListResponse(**response.json())
        assert len(result.data) == 2

        # 장소 조회
        place_pk = result.data[0].id
        response = await self.client.get(
            f"/api/place/{place_pk}",
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        PlaceResponse(**response.json())

    @pytest.mark.asyncio
    async def test_place_create_fail(self, create_root_user):
        access = create_root_user["data"]["access"]
        for params in [
            {},
            {"place_name": "장소1"},
            {"place_name": "장소2", "lat": 37.0, "lng": 127.0},
            {"place_name": "장소3", "lat": "text", "lng": "text", "tag_ids": []},
        ]:
            response = await self.client.post(
                "/api/place",
                json=params,
                headers={"Authorization": f"JWT {access}"},
            )
            assert response.status_code == 400
            CommonResponse(**response.json())

        response = await self.client.post(
            "/api/place",
            json={
                "place_name": "장소1",
                "lat": 37.0,
                "lng": 127.0,
                "tag_ids": [1, 2, 3]
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 404
        CommonResponse(**response.json())

    @pytest.mark.asyncio
    async def test_place_search_fail(self, create_root_user):
        access = create_root_user["data"]["access"]
        response = await self.client.get(
            "/api/place/999", headers={"Authorization": f"JWT {access}"}
        )
        assert response.status_code == 404
        CommonResponse(**response.json())
