from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.models.user import AuthUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get_user_with_tag_by_id(self, user_id: int):
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.id == user_id)
            .options(selectinload(AuthUser.tags))
        )
        return result.scalar_one()

    async def get_user_by_email(self, user_email: str) -> AuthUser | None:
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.user_email == user_email)
        )
        return result.scalars().first()

    async def get_user_by_user_name(self, user_name: str) -> AuthUser | None:
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.user_name == user_name)
        )
        return result.scalars().first()
