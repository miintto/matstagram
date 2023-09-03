from fastapi import Depends
from sqlalchemy.exc import NoResultFound

from app.common.exception import APIException
from app.domain.models.user import AuthUser
from app.common.response.codes import Http4XX
from app.domain.repository.user import UserRepository
from ..schemas.request import NewPasswordBody, UserInfoBody


class UserService:
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ):
        self.user_repository = user_repository

    async def get_user_info(self, user_id: int) -> dict:
        try:
            user = await self.user_repository.get_user_with_tag_by_id(user_id)
            return user.to_dict(load=True)
        except NoResultFound:
            raise APIException(Http4XX.USER_NOT_FOUND)

    async def _check_user_name_exists(
        self, user_name: str, user_id: int
    ) -> bool:
        user = await self.user_repository.get_user_by_user_name(user_name)
        if not user or user.id == user_id:
            return True
        raise APIException(Http4XX.DUPLICATED_USER_NAME, data=user_name)

    async def _check_user_email_exists(
        self, user_email: str, user_id: int
    ) -> bool:
        user = await self.user_repository.get_user_by_email(user_email)
        if not user or user.id == user_id:
            return True
        raise APIException(Http4XX.DUPLICATED_USER_EMAIL, data=user_email)

    async def update(
        self, user: AuthUser, body: UserInfoBody
    ) -> dict:
        await self._check_user_name_exists(body.user_name, user.id)
        await self._check_user_email_exists(body.user_email, user.id)
        user.user_name = body.user_name
        user.user_email = body.user_email
        if body.profile_image:
            user.profile_image = body.profile_image
        result = user.to_dict()
        await self.user_repository.save(user)
        return result

    async def change_password(
        self, user: AuthUser, body: NewPasswordBody
    ) -> bool:
        if not user.check_password(body.password):
            raise APIException(Http4XX.INVALID_PASSWORD)
        if body.new_password != body.new_password_check:
            raise APIException(Http4XX.MISMATCHED_PASSWORD)
        user.set_password(body.new_password)
        await self.user_repository.save(user)
        return True
