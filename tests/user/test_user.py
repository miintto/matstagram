import io
import os
import pytest

from PIL import Image
from sqlalchemy import select, update

from app.api.user.models import AuthUser, UserPermission
from app.api.user.schemas.response import (
    ImageUploadResponse,
    UserResponse,
    UserProfileResponse,
)
from app.common.schemas import CommonResponse, SuccessResponse
from tests.conftest import fixture_root_email, fixture_root_password
from tests.management.testcase import BaseTestCase


class TestUser(BaseTestCase):
    """사용자 정보 테스트"""

    @pytest.mark.asyncio
    async def test_user_search_success(self, create_root_user, session):
        access = create_root_user["data"]["access"]

        # 내 정보 조회
        response = await self.client.get(
            "api/user", headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        UserProfileResponse(**response.json())

        # 내 정보 수정
        new_name = "변경한 이름"
        new_email = "change@test.com"
        response = await self.client.patch(
            "api/user",
            json={"user_name": new_name, "user_email": new_email},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        user_res = UserResponse(**response.json())
        result = await session.execute(
            select(AuthUser).where(AuthUser.id == user_res.data.id)
        )
        user = result.scalar_one()
        assert user_res.data.user_name == new_name
        assert user_res.data.user_email == new_email
        assert user.user_name == new_name
        assert user.user_email == new_email

        new_password = "1234567890"
        response = await self.client.patch(
            "api/user/password",
            json={
                "password": fixture_root_password,
                "new_password": new_password,
                "new_password_check": new_password,
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        SuccessResponse(**response.json())

        # 다시 로그인 성공
        response = await self.client.post(
            url="/api/auth/login",
            json={
                "user_email": new_email,
                "password": new_password,
            },
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_info_change_fail(self, create_root_user, session):
        access = create_root_user["data"]["access"]
        session.add(AuthUser(user_name="user-1", user_email="user1@test.com"))
        await session.commit()

        # 존재하는 이름으로 뱐경
        response = await self.client.patch(
            "api/user",
            json={"user_name": "user-1", "user_email": "user-123@test.com"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

        # 존재하는 이메일로 뱐경
        response = await self.client.patch(
            "api/user",
            json={"user_name": "new-name", "user_email": "user1@test.com"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

    @pytest.mark.asyncio
    async def test_user_profile_image(self, create_root_user):
        access = create_root_user["data"]["access"]

        file = io.BytesIO()
        image = Image.new("RGBA", size=(5, 5), color=(0, 0, 0))
        image.save(file, "png")

        # 업로드 테스트
        response = await self.client.post(
            "api/user/image",
            files={'profile_image': ("test222.png", file, "image/png")},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 201
        result = ImageUploadResponse(**response.json())
        assert os.path.exists(f".{result.data}")
        os.remove(f".{result.data}")

        # 유효한 media-type 이 아니면 에러
        response = await self.client.post(
            "api/user/image",
            files={'profile_image': ("dump", io.BytesIO(), "image/svg+xml")},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

    @pytest.mark.asyncio
    async def test_user_password_change_fail(self, create_root_user):
        access = create_root_user["data"]["access"]

        # 기존 비밀번호 오류
        response = await self.client.patch(
            "api/user/password",
            json={
                "password": fixture_root_password + "123",
                "new_password": "12345",
                "new_password_check": "12345",
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

        # 새 비밀번호 불일치
        response = await self.client.patch(
            "api/user/password",
            json={
                "password": fixture_root_password,
                "new_password": "12345",
                "new_password_check": "123456789",
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

    @pytest.mark.asyncio
    async def test_user_profile(self, create_root_user, session):
        access = create_root_user["data"]["access"]
        user = AuthUser(user_name="user-2", user_email="user2@test.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # 일반 권한으로 사용자 조회
        response = await self.client.get(
            f"api/user/{user.id}", headers={"Authorization": f"JWT {access}"}
        )
        assert response.status_code == 403

        # 관리자 권한으로 사용자 조회
        await session.execute(
            update(AuthUser)
            .where(AuthUser.user_email == fixture_root_email)
            .values(user_permission=UserPermission.ADMIN)
        )
        await session.commit()
        await session.refresh(user)
        response = await self.client.get(
            f"api/user/{user.id}", headers={"Authorization": f"JWT {access}"}
        )
        assert response.status_code == 200
        UserProfileResponse(**response.json())

        # 없는 사용자 조회
        response = await self.client.get(
            f"api/user/999", headers={"Authorization": f"JWT {access}"}
        )
        assert response.status_code == 404
        CommonResponse(**response.json())
