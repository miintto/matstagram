import logging

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.common.exception import APIException
from app.common.response.codes import Http4XX, Http5XX
from app.common.types import ResultDict, ResultList
from app.domain.repository.place import PlaceRepository
from app.domain.repository.tag import TagRepository
from app.domain.models.place import Place
from app.domain.models.tag import PlaceTag
from app.domain.models.user import AuthUser
from ..schemas.request import PlaceRegisterBody
from ..serializers import PlaceSerializer

logger = logging.getLogger(__name__)


class PlaceService:
    def __init__(
        self,
        place_repository: PlaceRepository = Depends(PlaceRepository),
        tag_repository: TagRepository = Depends(TagRepository),
    ):
        self.place_repository = place_repository
        self.tag_repository = tag_repository

    async def get_place(self, place_id: int) -> ResultDict:
        data = await self.place_repository.get_place_by_id(place_id)
        if not data:
            raise APIException(Http4XX.PLACE_NOT_FOUND)
        return PlaceSerializer(data).serialize()[0]

    async def get_place_list(
        self, user_id: int, tags: str = None
    ) -> ResultList:
        tag_list = list(map(int, tags.split(","))) if tags else []
        data = await self.place_repository.get_place_list_with_tag_by_user(
            user_id, tag_ids=tag_list
        )
        return PlaceSerializer(data=data).serialize()

    async def _create_place(
        self, user: AuthUser, body: PlaceRegisterBody
    ) -> Place:
        try:
            place = Place(
                user_id=user.id,
                place_name=body.place_name,
                description=body.description,
                lat=body.lat,
                lng=body.lng,
            )
            await self.place_repository.flush(place)
        except IntegrityError as e:
            logger.error(f"장소 등록 실패 - body=({body}) error={e}")
            raise APIException(Http5XX.UNKNOWN_ERROR)
        return place

    async def _blind_tags(self, tag_ids: list, place_id: int):
        tag_count = await self.tag_repository.get_exists_tag_count(tag_ids)
        if tag_count != len(tag_ids):
            raise APIException(Http4XX.TAG_NOT_FOUND)

        await self.tag_repository.save(
            *(PlaceTag(place_id=place_id, tag_id=tag_id) for tag_id in tag_ids),
            refresh=False
        )

    async def register(
        self, user: AuthUser, body: PlaceRegisterBody
    ) -> ResultDict:
        place = await self._create_place(user, body)
        place_id = place.id
        if body.tag_ids:
            await self._blind_tags(body.tag_ids, place.id)
        result = await self.get_place(place_id)
        return result
