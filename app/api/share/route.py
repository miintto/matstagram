from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.place.schemas.resopnse import PlaceListResponse
from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.common.schemas import (
    PermissionDeniedResponse,
    UnauthenticatedResponse,
)
from app.common.security.permission import IsAuthenticated
from app.config.connection import db
from app.domain.models.user import AuthUser
from .schemas import ShareBody, ShareCreatedResponse
from .service import ShareService


router = APIRouter(prefix="/share", tags=["Share"])


@router.post(
    "",
    summary="내 맛집 공유하기",
    response_model=ShareCreatedResponse,
    status_code=201,
    responses={
        201: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def share_my_place(
    body: ShareBody,
    user: AuthUser = Depends(IsAuthenticated()),
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    사용자가 선택한 맛집 리스트를 공유합니다..
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await ShareService().generate(body, user, session),
    )



@router.get(
    "/place",
    summary="공유된 맛집 리스트 조회",
    response_model=PlaceListResponse,
    responses={
        200: {"description": "조회 성공."},
        401: {"description": "인증 실패", "model": UnauthenticatedResponse},
        403: {"description": "권한 없음", "model": PermissionDeniedResponse},
    },
)
async def get_place_list(
    k: str = Query(
        title="공유 id",
        description="공유하기로 생성된 문자열을 입력받습니다",
    ),
    tags: str | None = Query(
        title="태그 id",
        description="특정 태그가 달린 맛집들만 조회하는 경우에만 사용합니다.",
        default=None,
    ),
    session: AsyncSession = Depends(db.session),
) -> APIResponse:
    """
    사용자가 공유한 맛집 리스트를 조회합니다.
    """
    return APIResponse(
        Http2XX.SUCCESS,
        data=await ShareService().get_shared_place_list(k, tags, session),
    )
