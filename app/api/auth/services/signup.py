from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.security.jwt import JWTHandler
from app.common.types import ResultDict
from ..schemas import SignUpBody


class SignUp:
    @staticmethod
    async def _validate(body: SignUpBody, session: AsyncSession):
        result = await session.execute(
            select(AuthUser).where(AuthUser.user_email == body.user_email)
        )
        if result.scalars().first():
            raise APIException(
                Http4XX.DUPLICATED_USER_EMAIL, data=body.user_email
            )
        if body.password != body.password_check:
            raise APIException(Http4XX.MISMATCHED_PASSWORD)

    @staticmethod
    async def _create_user(
        body: SignUpBody, session: AsyncSession
    ) -> AuthUser:
        user = AuthUser(
            user_name=body.user_email,
            user_email=body.user_email,
            user_permission=UserPermission.NORMAL,
        )
        user.set_password(body.password)
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    def _generate_token(user: AuthUser) -> dict:
        handler = JWTHandler()
        return {
            "access": handler.generate_access_token(user),
            "refresh": handler.generate_refresh_token(user),
        }

    async def run(self, body: SignUpBody, session: AsyncSession) -> ResultDict:
        await self._validate(body, session)
        user = await self._create_user(body, session)
        token = self._generate_token(user)
        await session.commit()
        return token
