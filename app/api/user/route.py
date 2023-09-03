from fastapi import APIRouter, Depends

from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.common.schemas import (
    CommonResponse,
    PermissionDeniedResponse,
    SuccessResponse,
    UnauthenticatedResponse,
)
from app.common.security.permission import AdminOnly, IsNormalUser
from app.common.upload import upload_profile_image
from app.domain.models.user import AuthUser
from .schemas.request import NewPasswordBody, UserInfoBody
from .schemas.response import (
    ImageUploadResponse,
    UserResponse,
    UserProfileResponse,
)
from .services.user_profile import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "",
    summary="내 정보 조회",
    response_model=UserProfileResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def get_my_profile(
    user: AuthUser = Depends(IsNormalUser()),
    service: UserService = Depends(UserService),
) -> APIResponse:
    """
    사용자의 이메일, 이름, 권한 등의 정보를 조회합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS, data=await service.get_user_info(user_id=user.id)
    )


@router.patch(
    "",
    summary="내 정보 수정",
    response_model=UserResponse,
    responses={
        200: {"description": "정보 수정 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        422: {"description": "정보 수정 실패.", "model": CommonResponse},
    },
)
async def change_my_info(
    body: UserInfoBody,
    user: AuthUser = Depends(IsNormalUser()),
    service: UserService = Depends(UserService),
) -> APIResponse:
    return APIResponse(
        Http2XX.SUCCESS, data=await service.update(user, body)
    )


@router.post(
    "/image",
    summary="프로필 이미지 업로드",
    response_model=ImageUploadResponse,
    status_code=201,
    responses={
        201: {"description": "이미지 업로드 성공."},
        400: {"description": "업로드 실패.", "model": CommonResponse},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def upload_profile_image(
    profile_image: str = Depends(upload_profile_image),
    user: AuthUser = Depends(IsNormalUser()),
) -> APIResponse:
    return APIResponse(Http2XX.CREATED, data=profile_image)


@router.patch(
    "/password",
    summary="비밀번호 변경",
    response_model=SuccessResponse,
    responses={
        200: {"description": "비밀번호 변경 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        422: {"description": "비밀번호 변경 실패.", "model": CommonResponse},
    },
)
async def change_password(
    body: NewPasswordBody,
    user: AuthUser = Depends(IsNormalUser()),
    service: UserService = Depends(UserService),
) -> APIResponse:
    return APIResponse(
        Http2XX.SUCCESS,
        data=await service.change_password(user, body),
    )


@router.get(
    "/{pk}",
    summary="사용자 정보 조회",
    response_model=UserProfileResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        404: {"description": "조회 실패.", "model": CommonResponse},
    },
)
async def get_user_profile(
    pk: int,
    user: AuthUser = Depends(AdminOnly()),
    service: UserService = Depends(UserService),
) -> APIResponse:
    """
    특정 사용자의 정보를 조회합니다.

    관리자 권한으로 호출하는 경우만 조회가 가능합니다.
    """
    return APIResponse(Http2XX.SUCCESS, data=await service.get_user_info(pk))
