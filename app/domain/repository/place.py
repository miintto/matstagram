from typing import Sequence

from sqlalchemy import Row, select

from app.domain.models.place import Place
from app.domain.models.tag import PlaceTag, Tag
from .base import BaseRepository


class PlaceRepository(BaseRepository):
    async def get_place_by_id(self, place_id: int) -> Sequence[Row]:
        result = await self._session.execute(
            select(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .where(Place.id == place_id)
        )
        return result.all()

    async def get_place_list_with_tag_by_user(
        self, user_id: int, tag_ids: list = None
    ) -> Sequence[Row]:
        query = (
            select(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .where(Place.user_id == user_id)
            .order_by(Place.id, Tag.id)
        )
        if tag_ids:
            query = query.where(Tag.id.in_(tag_ids))
        result = await self._session.execute(query)
        return result.all()
