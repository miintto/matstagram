from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

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
from .schemas.response import UserResponse, UserProfileResponse
from .services.user_profile import UserProfile

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "",
    response_model=UserProfileResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def get_my_profile(
    user: AuthUser = Depends(IsNormalUser())
) -> APIResponse:
    """내 정보 조회"""
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict(load=True))


@router.patch(
    "",
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
    session: Session = Depends(db.session),
) -> APIResponse:
    """내 정보 수정"""
    return APIResponse(
        Http2XX.SUCCESS, data=UserProfile().update(user, body, session)
    )


@router.patch(
    "/image",
    response_model=UserResponse,
    responses={
        200: {"description": "이미지 변경 성공."},
        400: {"description": "정보 수정 실패.", "model": CommonResponse},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def change_my_profile_image(
    profile_image: str = Depends(upload_profile_image),
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """내 프로필 이미지 수정"""
    return APIResponse(
        Http2XX.SUCCESS,
        data=UserProfile().change_image(user, profile_image, session)
    )


@router.patch(
    "/password",
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
    session: Session = Depends(db.session),
) -> APIResponse:
    """비밀번호 변경"""
    return APIResponse(
        Http2XX.SUCCESS,
        data=UserProfile().change_password(user, body, session),
    )


@router.get(
    "/{pk}",
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
    session: Session = Depends(db.session),
) -> APIResponse:
    """사용자 정보 조회"""
    try:
        user = session.query(AuthUser).filter(AuthUser.id == pk).one()
    except NoResultFound:
        return APIResponse(Http4XX.USER_NOT_FOUND)
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict(load=True))
