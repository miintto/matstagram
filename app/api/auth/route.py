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
    summary="회원 가입",
    response_model=TokenResponse,
    responses={
        200: {"description": "성공."},
        422: {"description": "회원 가입 실패", "model": CommonResponse},
    },
)
async def sign_up(
    body: SignUpBody, session: Session = Depends(db.session)
) -> APIResponse:
    """
    정보를 입력받아 새로운 계정을 생성합니다.

    - [제약 조건]
        - 다른 사용자와 중복된 이메일은 사용할 수 없습니다.
        - 비밀번호는 숫자, 영문 대/소문자의 조합으로 길이는 8~20자 사이로 설정합니다.
    """
    return APIResponse(Http2XX.SUCCESS, data=SignUp().run(body, session))


@router.post(
    "/login",
    summary="로그인",
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
    """
    계정 정보를 입력받아서 일치하는 계정이 존재하면 인증 토큰을 반환합니다.
    """
    return APIResponse(Http2XX.SUCCESS, data=LogIn().run(body, session))
