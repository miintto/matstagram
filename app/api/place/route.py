from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser
from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.common.security.permission import IsAuthenticated, IsNormalUser
from app.config.connection import db
from .schemas import TagBody, PlaceRegisterBody
from .services.place import PlaceManager
from .services.tag import TagHandler

router = APIRouter(tags=["Place"])


@router.get("/place/{pk}")
async def get_place(
    pk: int,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 정보"""
    return APIResponse(
        Http2XX.SUCCESS, data=PlaceManager().get_place(user, pk, session)
    )


@router.get("/place")
async def get_place_list(
    user: AuthUser = Depends(IsAuthenticated()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 리스트"""
    return APIResponse(
        Http2XX.SUCCESS, data=PlaceManager().get_place_list(user, session)
    )


@router.post("/place", status_code=201)
async def register_place(
    body: PlaceRegisterBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """장소 등록"""
    PlaceManager().register(user, body, session)
    return APIResponse(Http2XX.CREATED)


@router.get("/tag")
async def tag_list(
    user: AuthUser = Depends(IsAuthenticated()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """태그 리스트"""
    return APIResponse(
        Http2XX.SUCCESS, data=TagHandler.get_user_tag_list(user, session)
    )


@router.post("/tag", status_code=201)
async def create_tag(
    body: TagBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """태그 등록"""
    return APIResponse(
        Http2XX.CREATED, data=TagHandler().create(user, body, session)
    )


@router.post("/tag/{pk}")
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
