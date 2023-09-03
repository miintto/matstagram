import uuid

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.place import Place
from app.domain.models.tag import PlaceTag, Tag
from app.api.place.serializers import PlaceSerializer
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.types import ResultList
from app.domain.models.user import AuthUser
from app.domain.models.location import Location, PlaceLocation
from app.domain.models.share import Share, ShareLocation
from .schemas import ShareBody


class ShareService:
    @staticmethod
    async def _create_share(body: ShareBody, user_pk: int) -> Share:
        return Share(
            key=uuid.uuid4().hex[:20],
            user_id=user_pk,
            description=body.description,
            lat=body.lat,
            lng=body.lng,
        )

    async def generate(
        self, body: ShareBody, user: AuthUser, session: AsyncSession
    ) -> str:
        """다른 사람에게 공유 가능하도록 데이터를 생성합니다."""
        share = await self._create_share(body, user.id)
        session.add(share)
        await session.flush()
        for location_id in body.locations:
            session.add(
                ShareLocation(share_id=share.id, location_id=location_id)
            )
        key = share.key
        await session.commit()
        return key

    @staticmethod
    async def _get_owners_pk(key: str, session: AsyncSession) -> int:
        try:
            result = await session.execute(
                select(Share).where(
                    Share.key == key, Share.is_active.is_(True)
                )
            )
            share = result.scalar_one()
            return share.user_id
        except NoResultFound:
            raise APIException(Http4XX.SHARE_NOT_FOUND)

    async def get_shared_place_list(
        self, key: str, tags: str, session: AsyncSession
    ) -> ResultList:
        """공유된 맛집들을 조회합니다."""
        user_pk = await self._get_owners_pk(key, session)
        query = (
            select(Place, Tag)
            .join(PlaceLocation, PlaceLocation.place_id == Place.id)
            .join(Location, Location.id == PlaceLocation.location_id)
            .join(ShareLocation, ShareLocation.location_id == Location.id)
            .join(Share, Share.id == ShareLocation.share_id)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .where(
                Place.user_id == user_pk,
                Share.user_id == user_pk,
                Share.key == key,
            )
            .order_by(Place.id, Tag.id)
        )
        if tags:
            query = query.where(Tag.id.in_(list(map(int, tags.split(",")))))
        result = await session.execute(query)
        return PlaceSerializer(data=result.fetchall()).serialize()
