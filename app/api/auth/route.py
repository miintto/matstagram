from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import APIResponse
from app.common.response.codes import Http2XX
from app.config.connection import db
from .schemas import LogInBody, SignUpBody, TokenResponse
from .services.login import LogIn
from .services.signup import SignUp

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
async def sign_up(
    body: SignUpBody, session: Session = Depends(db.session)
) -> APIResponse:
    """회원가입"""
    return APIResponse(Http2XX.CREATED, data=SignUp().run(body, session))


@router.post("/login", response_model=TokenResponse)
async def log_in(
    body: LogInBody, session: Session = Depends(db.session)
) -> APIResponse:
    """로그인"""
    return APIResponse(Http2XX.SUCCESS, data=LogIn().run(body, session))
