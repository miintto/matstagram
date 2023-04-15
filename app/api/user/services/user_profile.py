from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import APIException
from app.common.response.codes import Http4XX
from ..models import AuthUser
from ..schemas.request import NewPasswordBody, UserInfoBody


class UserProfile:
    async def _validate_user_name(
        self, user_name: str, user_pk: int, session: AsyncSession
    ) -> bool:
        result = await session.execute(
            select(AuthUser).where(
                AuthUser.user_name == user_name, AuthUser.id != user_pk
            )
        )
        if result.scalars().first():
            raise APIException(Http4XX.DUPLICATED_USER_NAME, data=user_name)
        return True

    async def _validate_user_email(
        self, user_email: str, user_pk: int, session: AsyncSession
    ) -> bool:
        result = await session.execute(
            select(AuthUser).where(
                AuthUser.user_email == user_email, AuthUser.id != user_pk
            )
        )
        if result.scalars().first():
            raise APIException(Http4XX.DUPLICATED_USER_EMAIL, data=user_email)
        return True

    async def update(
        self, user: AuthUser, body: UserInfoBody, session: AsyncSession
    ) -> dict:
        await self._validate_user_name(body.user_name, user.id, session)
        await self._validate_user_email(body.user_email, user.id, session)
        user.user_name = body.user_name
        user.user_email = body.user_email
        if body.profile_image:
            user.profile_image = body.profile_image
        result = user.to_dict()
        await session.commit()
        return result

    async def change_password(
        self, user: AuthUser, body: NewPasswordBody, session: AsyncSession
    ) -> bool:
        if not user.check_password(body.password):
            raise APIException(Http4XX.INVALID_PASSWORD)
        if body.new_password != body.new_password_check:
            raise APIException(Http4XX.MISMATCHED_PASSWORD)
        user.set_password(body.new_password)
        await session.commit()
        return True
