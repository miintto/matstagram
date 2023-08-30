import logging

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.models import AuthUser
from app.common.exception import APIException
from app.common.response.codes import Http4XX, Http5XX
from app.common.types import ResultDict, ResultList
from ..models import Place, PlaceTag, Tag
from ..schemas.request import PlaceRegisterBody
from ..serializers import PlaceSerializer

logger = logging.getLogger(__name__)


class PlaceManager:
    async def get_place(
        self, user_pk: int, place_id: int, session: AsyncSession
    ) -> ResultDict:
        result = await session.execute(
            select(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .where(Place.id == place_id, Place.user_id == user_pk)
        )
        data = result.fetchall()
        if not data:
            raise APIException(Http4XX.PLACE_NOT_FOUND)
        return PlaceSerializer(data).serialize()[0]

    async def get_place_list(
        self, user_pk: int, tags: str, session: AsyncSession
    ) -> ResultList:
        query = (
            select(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .where(Place.user_id == user_pk)
            .order_by(Place.id, Tag.id)
        )
        if tags:
            query = query.where(Tag.id.in_(list(map(int, tags.split(",")))))
        result = await session.execute(query)
        data = result.fetchall()
        return PlaceSerializer(data=data).serialize()

    async def _create_place(
        self, user: AuthUser, body: PlaceRegisterBody, session: AsyncSession
    ) -> Place:
        try:
            place = Place(
                user_id=user.id,
                place_name=body.place_name,
                description=body.description,
                lat=body.lat,
                lng=body.lng,
            )
            session.add(place)
            await session.flush()
        except IntegrityError as e:
            logger.error(f"장소 등록 실패 - body=({body}) error={e}")
            raise APIException(Http5XX.UNKNOWN_ERROR)
        return place

    async def _create_tag(
        self, tag_ids: list, place_id: int, session: AsyncSession
    ):
        result = await session.execute(
            select(func.count(Tag.id)).where(Tag.id.in_(tag_ids))
        )
        if result.scalar_one() != len(tag_ids):
            raise APIException(Http4XX.TAG_NOT_FOUND)
        for tag_id in tag_ids:
            place_tag = PlaceTag(place_id=place_id, tag_id=tag_id)
            session.add(place_tag)
        await session.flush()

    async def register(
        self, user: AuthUser, body: PlaceRegisterBody, session: AsyncSession
    ) -> ResultDict:
        place = await self._create_place(user, body, session)
        if body.tag_ids:
            await self._create_tag(body.tag_ids, place.id, session)
        result = await self.get_place(user.id, place.id, session)
        await session.commit()
        return result
