from typing import TypedDict

from pydantic import BaseModel, EmailStr

from app.common.schemas import CommonResponse


class SignUpBody(BaseModel):
    """회원 가입 body"""

    user_email: EmailStr
    password: str
    password_check: str


class TokenData(TypedDict):
    access: str
    refresh: str


class TokenResponse(CommonResponse):
    """발급한 토큰 응답 response"""

    data: TokenData


class LogInBody(BaseModel):
    """로그인 body"""

    user_email: str
    password: str
