from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
    summary="맛집 정보 조회",
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    특정 맛집에 대한 상세 정보를 반환합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS, data=await PlaceManager().get_place(user, pk, session)
    )


@router.get(
    "/place",
    summary="맛집 리스트 조회",
    response_model=PlaceListResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def get_place_list(
    tags: str | None = Query(
        title="태그 id",
        description="특정 태그가 달린 맛집들만 조회하는 경우에만 사용합니다.",
        default=None,
    ),
    user: AuthUser = Depends(IsAuthenticated()),
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    사용자가 등록한 맛집 리스트를 조회합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await PlaceManager().get_place_list(user, tags, session),
    )


@router.post(
    "/place",
    summary="맛집 등록",
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """맛집을 등록합니다."""
    return APIResponse(
        Http2XX.CREATED,
        data=await PlaceManager().register(user, body, session),
    )


@router.get(
    "/tag",
    summary="태그 리스트 조회",
    response_model=TagListResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def tag_list(
    user: AuthUser = Depends(IsAuthenticated()),
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    사용자가 등록한 태그 목록을 조회합니다.

    만일 등록돤 태그가 하나도 없는 경우 `data` 의 반환값으로 빈 array (`[]`) 를 반환합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await TagHandler.get_user_tag_list(user, session)
    )


@router.post(
    "/tag",
    summary="태그 생성",
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    태그 정보를 입력받아 사용자의 태그를 생성합니다.
    """
    return APIResponse(
        Http2XX.CREATED, data=await TagHandler().create(user, body, session)
    )


@router.post(
    "/tag/{pk}",
    summary="태그 수정",
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
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    태그 정보를 수정합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await TagHandler().update(user.id, pk, body, session),
    )
