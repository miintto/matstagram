from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.common.response import APIResponse
from app.common.response.codes import Http2XX, Http4XX
from app.common.security.permission import AdminOnly, IsNormalUser
from app.config.connection import db
from .models import AuthUser
from .schemas import NewPasswordBody, UserInfoBody
from .services.user_profile import UserProfile

router = APIRouter(prefix="/user", tags=["User"])


@router.get("")
async def get_my_profile(
    user: AuthUser = Depends(IsNormalUser())
) -> APIResponse:
    """내 정보 조회"""
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict())


@router.patch("")
async def change_my_info(
    body: UserInfoBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """내 정보 수정"""
    return APIResponse(
        Http2XX.SUCCESS, data=UserProfile().update(user, body, session)
    )


@router.patch("")
async def change_password(
    body: NewPasswordBody,
    user: AuthUser = Depends(IsNormalUser()),
    session: Session = Depends(db.session),
) -> APIResponse:
    """내 정보 수정"""
    return APIResponse(
        Http2XX.SUCCESS,
        data=UserProfile().change_password(user, body, session),
    )


@router.get("/{pk}")
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
    return APIResponse(Http2XX.SUCCESS, data=user.to_dict())
