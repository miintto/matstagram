from pydantic import BaseModel, EmailStr, Field


class UserInfoBody(BaseModel):
    user_name: str = Field(title="사용자 이름", description="변경할 사용자 이름.")
    user_email: EmailStr = Field(
        title="사용자 이메일",
        description="변경할 사용자 이메일. 다른 사용자가 사용중인 이메일로 변경은 불가능합니다."
    )
    profile_image: str | None = Field(
        title="사용자 프로필 이미지", description="업로드된 프로필 이미지 파일 경로"
    )


class NewPasswordBody(BaseModel):
    password: str = Field(
        title="현재 비밀번호",
        description="현재 반영되어 있는 비밀번호를 입력합니다.",
        example="aBCdefg123",
    )
    new_password: str = Field(
        title="새 비밀번호",
        description="새로 설정할 비밀번호. 숫자, 영문 대/소문자의 조합으로 사용할 수 있습니다.",
        example="987xyZ00",
    )
    new_password_check: str = Field(
        title="새 비밀번호 확인",
        description="새로 설정한 비밀번호를 한 번 더 입력합니다.",
        example="987xyZ00",
    )