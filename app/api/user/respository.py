from sqlalchemy import select

from app.api.user.models import AuthUser
from app.common.repository import BaseRepository


class UserRepository(BaseRepository):

    async def get_user_by_email(self, user_email: str) -> AuthUser | None:
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.user_email == user_email)
        )
        return result.scalars().first()
