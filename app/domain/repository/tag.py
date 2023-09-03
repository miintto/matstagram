from sqlalchemy import ScalarResult, func, select

from app.domain.models.tag import Tag
from .base import BaseRepository


class TagRepository(BaseRepository):
    async def get_tag_by_id(self, tag_id: int) -> Tag:
        result = await self._session.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return result.scalar_one()

    async def get_tag_list_by_user(self, user_id: int) -> ScalarResult[Tag]:
        result = await self._session.execute(
            select(Tag).where(Tag.user_id == user_id)
        )
        return result.scalars()

    async def get_exists_tag_count(self, tag_ids: list) -> int:
        result = await self._session.execute(
            select(func.count(Tag.id)).where(Tag.id.in_(tag_ids))
        )
        return result.scalar_one()
