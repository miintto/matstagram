from pydantic import BaseModel, EmailStr, Field

from app.common.schemas import SuccessResponse


class SignUpBody(BaseModel):
    """회원 가입 body"""

    user_email: EmailStr = Field(
        title="사용자 이메일", description="로그인시 사용할 이메일"
    )
    password: str = Field(
        title="비밀번호", description="로그인시 사용할 비밀 번호", example="aBCdefg123"
    )
    password_check: str = Field(
        title="비밀번호 확인",
        description="정합성을 위해서 같은 비밀번호를 한 번 더 입력합니다.",
        example="aBCdefg123",
    )


class TokenData(BaseModel):
    access: str = Field(title="Access 토큰", example="eyJhbGciOiJIUzI...")
    refresh: str = Field(title="Refresh 토큰", example="eyJ0eXBlIjoicmV...")


class TokenResponse(SuccessResponse):
    """발급한 토큰 응답"""

    data: TokenData


class LogInBody(BaseModel):
    """로그인 body"""

    user_email: EmailStr = Field(title="사용자 이메일", description="가입한 이메일")
    password: str = Field(
        title="비밀번호", description="가입시 설정한 비밀번호", example="aBCdefg123"
    )
