from fastapi import Depends

from app.api.user.models import AuthUser, UserPermission
from app.api.user.respository import UserRepository
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.jwt import JWTHandler
from app.common.types import ResultDict
from ..schemas import SignUpBody


class SignUpService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def _validate(self, body: SignUpBody):
        user = await self.user_repository.get_user_by_email(body.user_email)
        if user:
            raise APIException(
                Http4XX.DUPLICATED_USER_EMAIL, data=body.user_email
            )
        if body.password != body.password_check:
            raise APIException(Http4XX.MISMATCHED_PASSWORD)

    async def _create_user(self, body: SignUpBody) -> AuthUser:
        user = AuthUser(
            user_name=body.user_email,
            user_email=body.user_email,
            user_permission=UserPermission.NORMAL,
        )
        user.set_password(body.password)
        return await self.user_repository.save(user, refresh=True)

    @staticmethod
    def _generate_token(user: AuthUser) -> dict:
        handler = JWTHandler()
        return {
            "access": handler.generate_access_token(user),
            "refresh": handler.generate_refresh_token(user),
        }

    async def run(self, body: SignUpBody) -> ResultDict:
        await self._validate(body)
        user = await self._create_user(body)
        token = self._generate_token(user)
        return token
