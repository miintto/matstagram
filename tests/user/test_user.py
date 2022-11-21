from app.api.user.models import AuthUser
from app.api.user.schemas.response import UserResponse, UserProfileResponse
from app.common.schemas import CommonResponse, SuccessResponse
from ..management.fixtures import PyTestFixtures
from ..testcase import BaseTestCase


class TestUser(BaseTestCase, PyTestFixtures):
    """사용자 정보 테스트"""

    def test_user_search_success(self, create_root_user, session):
        access = create_root_user["data"]["access"]

        # 내 정보 조회
        response = self.client.get(
            "api/user", headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        UserProfileResponse(**response.json())

        # 내 정보 수정
        new_name = "변경한 이름"
        new_email = "change@test.com"
        response = self.client.patch(
            "api/user",
            json={"user_name": new_name, "user_email": new_email},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        result = UserResponse(**response.json())
        user = session.query(AuthUser).filter(
            AuthUser.id == result.data.get("id")
        ).one()
        assert result.data.get("user_name") == new_name
        assert result.data.get("user_email") == new_email
        assert user.user_name == new_name
        assert user.user_email == new_email

        new_password = "1234567890"
        response = self.client.patch(
            "api/user/password",
            json={
                "password": self.fixture_root_password,
                "new_password": new_password,
                "new_password_check": new_password
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 200
        SuccessResponse(**response.json())

        # 다시 로그인 성공
        response = self.client.post(
            url="/api/auth/login",
            json={
                "user_email": new_email,
                "password": new_password,
            },
        )
        assert response.status_code == 200

    def test_user_info_change_fail(self, create_root_user, session):
        access = create_root_user["data"]["access"]
        session.add(AuthUser(user_name="user-1", user_email="user1@test.com"))
        session.commit()

        # 존재하는 이름으로 뱐경
        response = self.client.patch(
            "api/user",
            json={"user_name": "user-1", "user_email": "user-123@test.com"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

        # 존재하는 이메일로 뱐경
        response = self.client.patch(
            "api/user",
            json={"user_name": "new-name", "user_email": "user1@test.com"},
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

    def test_user_password_change_fail(self, create_root_user, session):
        access = create_root_user["data"]["access"]

        # 기존 비밀번호 오류
        response = self.client.patch(
            "api/user/password",
            json={
                "password": self.fixture_root_password + "123",
                "new_password": "12345",
                "new_password_check": "12345",
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())

        # 새 비밀번호 불일치
        response = self.client.patch(
            "api/user/password",
            json={
                "password": self.fixture_root_password,
                "new_password": "12345",
                "new_password_check": "123456789",
            },
            headers={"Authorization": f"JWT {access}"},
        )
        assert response.status_code == 422
        CommonResponse(**response.json())
