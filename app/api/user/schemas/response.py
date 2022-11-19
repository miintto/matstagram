from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, EmailStr

from app.api.user.models import UserPermission
from app.common.schemas import SuccessResponse


class User(TypedDict):
    id: int
    user_name: str
    user_email: EmailStr
    user_permission: UserPermission
    is_active: bool
    created_dtm: datetime
    last_login_dtm: datetime


class UserResponse(SuccessResponse):
    """사용자 응답"""

    data: User
