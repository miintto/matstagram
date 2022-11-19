from typing import TypedDict

from pydantic import BaseModel, EmailStr

from app.common.schemas import SuccessResponse


class SignUpBody(BaseModel):
    """회원 가입 body"""

    user_email: EmailStr
    password: str
    password_check: str


class TokenData(TypedDict):
    access: str
    refresh: str


class TokenResponse(SuccessResponse):
    """발급한 토큰 응답"""

    data: TokenData


class LogInBody(BaseModel):
    """로그인 body"""

    user_email: EmailStr
    password: str
