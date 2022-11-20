from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser
from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.common.schemas import (
    CommonResponse,
    PermissionDeniedResponse,
    UnauthenticatedResponse
)
from app.common.security.permission import IsAuthenticated, IsNormalUser
from app.config.connection import db
from .schemas.request import PlaceRegisterBody, TagBody
from .schemas.resopnse import (
    PlaceCreatedResponse,
    PlaceListResponse,
    PlaceResponse,
    TagCreatedResponse,
    TagListResponse,
    TagResponse,
)
from .services.place import PlaceManager
from .services.tag import TagHandler

router = APIRouter(tags=["Place"])


@router.get(
    "/place/{pk}",
    response_model=PlaceResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        404: {"description": "조회 실패", "model": CommonResponse},
    },
)
async def get_place(
    pk: int,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 정보"""
    return APIResponse(
        Http2XX.SUCCESS, data=PlaceManager().get_place(user, pk, session)
    )


@router.get(
    "/place",
    response_model=PlaceListResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def get_place_list(
    tags: str | None = None,
    user: AuthUser = Depends(IsAuthenticated()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 리스트"""
    return APIResponse(
        Http2XX.SUCCESS,
        data=PlaceManager().get_place_list(user, tags, session),
    )


@router.post(
    "/place",
    response_model=PlaceCreatedResponse,
    status_code=201,
    responses={
        201: {"description": "장소 등록 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        404: {"description": "태그 조회 실패", "model": CommonResponse},
    },
)
async def register_place(
    body: PlaceRegisterBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 등록"""
    return APIResponse(
        Http2XX.CREATED, data=PlaceManager().register(user, body, session)
    )


@router.get(
    "/tag",
    response_model=TagListResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def tag_list(
    user: AuthUser = Depends(IsAuthenticated()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """태그 리스트"""
    return APIResponse(
        Http2XX.SUCCESS, data=TagHandler.get_user_tag_list(user, session)
    )


@router.post(
    "/tag",
    response_model=TagCreatedResponse,
    status_code=201,
    responses={
        201: {"description": "태그 생성 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def create_tag(
    body: TagBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """태그 생성"""
    return APIResponse(
        Http2XX.CREATED, data=TagHandler().create(user, body, session)
    )


@router.post(
    "/tag/{pk}",
    response_model=TagResponse,
    responses={
        200: {"description": "태그 수정 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
        404: {"description": "태그 조회 실패.", "model": CommonResponse},
    },
)
async def update_tag(
    pk: int,
    body: TagBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """태그 수정"""
    return APIResponse(
        Http2XX.SUCCESS, data=TagHandler().update(user, pk, body, session)
    )
