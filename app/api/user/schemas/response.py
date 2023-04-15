from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.api.place.schemas.resopnse import Tag
from app.api.user.models import UserPermission
from app.common.schemas import CreatedResponse, SuccessResponse


class User(BaseModel):
    id: int = Field(title="Primary Key", description="사용자 pk", example=16)
    user_name: str = Field(title="사용자 이름", example="김철수")
    user_email: EmailStr = Field(title="사용자 이메일")
    user_permission: UserPermission = Field(
        title="사용자 권한",
        description="`anonymous`: 비회원 / `normal`: 일반 사용자 / `admin`: 관리자",
        example="normal",
        type="string",
    )
    profile_image: str | None = Field(
        title="프로필 이미지",
        description="프로필 이미지 파일 경로",
        example="/static/img/profile.png",
    )
    is_active: bool = Field(
        title="활성화 여부",
        description="`true`: 활성화 / `false`: 비활성화",
    )
    created_dtm: datetime = Field(
        title="사용자 생성 일시",
        pattern="YYYY-MM-DD HH:Mi:SS.ffffff",
        example="2019-09-04 14:15:22.115814",
    )
    last_login_dtm: datetime | None = Field(
        title="마지막 로그인 일시",
        pattern="YYYY-MM-DD HH:Mi:SS.ffffff",
        example="2022-06-10 10:29:42.257399",
    )


class UserProfile(User):
    tags: list[Tag] = Field(title="사용자 등록 태그 리스트")


class UserResponse(SuccessResponse):
    """사용자 응답"""

    data: User


class UserProfileResponse(SuccessResponse):
    """사용자 응답"""

    data: UserProfile


class ImageUploadResponse(CreatedResponse):
    """이미지 업로드 성공 응답"""

    data: str
