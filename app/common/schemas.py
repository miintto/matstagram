from typing import Any, Literal

from pydantic import BaseModel


class CommonResponse(BaseModel):
    code: str
    message: str
    data: Any


class SuccessResponse(CommonResponse):
    """성공 응답"""

    code: Literal["S000"]
    message: Literal["성공"]


class CreatedResponse(CommonResponse):
    """생성 왼료 응답"""

    code: Literal["S001"]
    message: Literal["생성 완료"]


class UnauthenticatedResponse(CommonResponse):
    """인증 실패 응답"""

    code: Literal["F001"]
    message: Literal["잘못된 인증 정보입니다."]


class PermissionDeniedResponse(CommonResponse):
    """권한 없음 응답"""

    code: Literal["F002"]
    message: Literal["권한이 없습니다."]
