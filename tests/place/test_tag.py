from app.api.place.models import Tag
from app.api.place.schemas.resopnse import (
    TagCreatedResponse,
    TagListResponse,
    TagResponse,
    PlaceCreatedResponse,
    PlaceListResponse,
)
from app.common.schemas import CommonResponse
from tests.management.fixtures import PyTestFixtures
from tests.management.testcase import BaseTestCase


class TestTag(BaseTestCase, PyTestFixtures):
    """태그 테스트"""

    def test_tag_success(self, create_root_user, session):
        access = create_root_user["data"]["access"]
        # 태그 생성
        response = self.client.post(
            "/api/tag",
            json={"tag_name": "태그1", "memo": "첫 번째 태그"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        TagCreatedResponse(**response.json())

        # memo 없어도 생성
        response = self.client.post(
            "/api/tag",
            json={"tag_name": "태그2"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        result = TagCreatedResponse(**response.json())

        # 태그 수정
        tag_id = result.data.get("id")
        new_tag_name = "태그2-수정"
        response = self.client.post(
            f"/api/tag/{tag_id}",
            json={"tag_name": new_tag_name},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        result = TagResponse(**response.json())
        tag = session.query(Tag).filter(Tag.id == tag_id).one()
        assert tag.tag_name == new_tag_name
        assert result.data.get("tag_name") == new_tag_name

        response = self.client.get(
            f"/api/tag",
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        result = TagListResponse(**response.json())
        assert len(result.data) == 2

    def test_tag_create_fail(self, create_root_user):
        access = create_root_user["data"]["access"]
        for params in [{}, {"memo": "메모메모"}]:
            response = self.client.post(
                "/api/tag",
                json=params,
                headers={"Authorization": f"JWT {access}"},
            )
            assert response.status_code == 400
            CommonResponse(**response.json())

    def test_place_with_tag(self, create_root_user):
        access = create_root_user["data"]["access"]
        tag_list = []
        # 태그 생성
        response = self.client.post(
            "/api/tag",
            json={"tag_name": "장소용 태그1"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        result = TagCreatedResponse(**response.json())
        tag_list.append(result.data.get("id"))

        response = self.client.post(
            "/api/tag",
            json={"tag_name": "장소용 태그2"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        result = TagCreatedResponse(**response.json())
        tag_list.append(result.data.get("id"))

        assert len(tag_list) == 2

        # 장소 등록
        response = self.client.post(
            "/api/place",
            json={
                "place_name": "장소1",
                "lat": 37.0,
                "lng": 127.0,
                "tag_ids": tag_list,
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        result = PlaceCreatedResponse(**response.json())
        assert len(result.data.get("tags")) == 2

        # 태그로 장소 리스트 조회
        response = self.client.get(
            "/api/place",
            data={"tags": ",".join(map(str, tag_list))},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        result = PlaceListResponse(**response.json())
        assert len(result.data) == 1
