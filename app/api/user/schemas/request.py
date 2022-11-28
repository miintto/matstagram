from pydantic import BaseModel, EmailStr


class UserInfoBody(BaseModel):
    user_name: str
    user_email: EmailStr
    profile_image: str | None


class NewPasswordBody(BaseModel):
    password: str
    new_password: str
    new_password_check: str
