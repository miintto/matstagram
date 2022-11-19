from pydantic import BaseModel, EmailStr


class UserInfoBody(BaseModel):
    user_name: str | None
    user_email: EmailStr | None


class NewPasswordBody(BaseModel):
    password: str
    new_password: str
    new_password_check: str