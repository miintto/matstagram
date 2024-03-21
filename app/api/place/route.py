from fastapi import APIRouter, Depends, Query

from app.common.http.codes import Http2XX
from app.common.http.response import APIResponse
from app.common.schemas import (
    CommonResponse,
    PermissionDeniedResponse,
    UnauthenticatedResponse,
)
from app.common.security.permission import IsAuthenticated, IsNormalUser
from app.domain.models.user import AuthUser
from .schemas.request import PlaceRegisterBody, TagBody
from .schemas.resopnse import (
    PlaceCreatedResponse,
    PlaceListResponse,
    PlaceResponse,
    TagCreatedResponse,
    TagListResponse,
    TagResponse,
)
from .services.place import PlaceService
from .services.tag import TagService

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
    service: PlaceService = Depends(PlaceService),
) -> APIResponse:
    """
    특정 맛집에 대한 상세 정보를 반환합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await service.get_place(pk),
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
    service: PlaceService = Depends(PlaceService),
) -> APIResponse:
    """
    사용자가 등록한 맛집 리스트를 조회합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await service.get_place_list(user.id, tags),
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
    service: PlaceService = Depends(PlaceService),
) -> APIResponse:
    """맛집을 등록합니다."""
    return APIResponse(
        Http2XX.CREATED,
        data=await service.register(user, body),
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
    service: TagService = Depends(TagService),
) -> APIResponse:
    """
    사용자가 등록한 태그 목록을 조회합니다.

    만일 등록돤 태그가 하나도 없는 경우 `data` 의 반환값으로 빈 array (`[]`) 를 반환합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS, data=await service.get_user_tag_list(user)
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
    service: TagService = Depends(TagService),
) -> APIResponse:
    """
    태그 정보를 입력받아 사용자의 태그를 생성합니다.
    """
    return APIResponse(
        Http2XX.CREATED, data=await service.create(user, body)
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
    service: TagService = Depends(TagService),
) -> APIResponse:
    """
    태그 정보를 수정합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await service.update(user.id, pk, body),
    )
