from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.common.schemas import CommonResponse
from app.config.connection import db
from .schemas import LogInBody, SignUpBody, TokenResponse
from .services.login import LogIn
from .services.signup import SignUp

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=TokenResponse,
    responses={
        200: {"description": "성공."},
        422: {"description": "회원 가입 실패", "model": CommonResponse},
    },
)
async def sign_up(
    body: SignUpBody, session: Session = Depends(db.session)
) -> APIResponse:
    """회원 가입"""
    return APIResponse(Http2XX.SUCCESS, data=SignUp().run(body, session))


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        200: {"description": "성공."},
        400: {"description": "파라미터 에러", "model": CommonResponse},
        404: {"description": "이메일 불일치", "model": CommonResponse},
        422: {"description": "비밀번호 불일치", "model": CommonResponse},
    },
)
async def log_in(
    body: LogInBody, session: Session = Depends(db.session)
) -> APIResponse:
    """로그인"""
    return APIResponse(Http2XX.SUCCESS, data=LogIn().run(body, session))
