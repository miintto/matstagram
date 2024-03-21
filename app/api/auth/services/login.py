from fastapi import Depends

from app.common.exception import APIException
from app.common.http.codes import Http4XX
from app.common.security.jwt import JWTHandler
from app.common.types import ResultDict
from app.domain.models.user import AuthUser
from app.domain.repository.user import UserRepository
from ..schemas import LogInBody


class LogInService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def _get_user(self, user_email: str) -> AuthUser:
        user = await self.user_repository.get_user_by_email(user_email)
        if not user or not user.is_active:
            raise APIException(Http4XX.USER_NOT_FOUND)
        return user

    @staticmethod
    def _generate_token(user: AuthUser) -> dict:
        handler = JWTHandler()
        return {
            "access": handler.generate_access_token(user),
            "refresh": handler.generate_refresh_token(user),
        }

    async def run(self, body: LogInBody) -> ResultDict:
        user = await self._get_user(body.user_email)
        if not user.check_password(body.password):
            raise APIException(Http4XX.INVALID_PASSWORD)
        return self._generate_token(user)
