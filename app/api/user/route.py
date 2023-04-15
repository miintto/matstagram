from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.common.response import APIResponse
from app.common.response.codes import Http2XX, Http4XX
from app.common.schemas import (
    CommonResponse,
    PermissionDeniedResponse,
    SuccessResponse,
    UnauthenticatedResponse,
)
from app.common.security.permission import AdminOnly, IsNormalUser
from app.common.upload import upload_profile_image
from app.config.connection import db
from .models import AuthUser
from .schemas.request import NewPasswordBody, UserInfoBody
from .schemas.response import (
    ImageUploadResponse,
    UserResponse,
    UserProfileResponse,
)
from .services.user_profile import UserProfile

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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    사용자의 이메일, 이름, 권한 등의 정보를 조회합니다.
    """
    await session.refresh(user, attribute_names=["tags"])
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict(load=True))


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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    return APIResponse(
        Http2XX.SUCCESS, data=await UserProfile().update(user, body, session)
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    return APIResponse(
        Http2XX.SUCCESS,
        data=UserProfile().change_password(user, body, session),
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    특정 사용자의 정보를 조회합니다.

    관리자 권한으로 호출하는 경우만 조회가 가능합니다.
    """
    try:
        result = await session.execute(
            select(AuthUser).where(AuthUser.id == pk)
            .options(selectinload(AuthUser.tags))
        )
        user = result.scalar_one()
    except NoResultFound:
        return APIResponse(Http4XX.USER_NOT_FOUND)
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict(load=True))
