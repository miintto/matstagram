from datetime import datetime
from typing import TypedDict

from pydantic import EmailStr

from app.api.place.schemas.resopnse import Tag
from app.api.user.models import UserPermission
from app.common.schemas import SuccessResponse


class User(TypedDict):
    id: int
    user_name: str
    user_email: EmailStr
    user_permission: UserPermission
    is_active: bool
    created_dtm: datetime
    last_login_dtm: datetime | None


class UserProfile(User):
    tags: list[Tag]


class UserResponse(SuccessResponse):
    """사용자 응답"""

    data: User


class UserProfileResponse(SuccessResponse):
    """사용자 응답"""

    data: UserProfile
