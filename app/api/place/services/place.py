import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser
from app.common.exception import APIException
from app.common.response.codes import Http4XX, Http5XX
from app.common.types import ResultDict, ResultList
from ..models import Place, PlaceTag, Tag
from ..schemas.request import PlaceRegisterBody
from ..serializers import PlaceSerializer

logger = logging.getLogger(__name__)


class PlaceManager:
    def get_place(
        self, user: AuthUser, place_id: int, session: Session
    ) -> ResultDict:
        data = (
            session.query(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .filter(Place.id == place_id, Place.user_id == user.id)
            .all()
        )
        if not data:
            raise APIException(Http4XX.PLACE_NOT_FOUND)
        return PlaceSerializer(data).serialize()[0]

    def get_place_list(
        self, user: AuthUser, tags: str, session: Session
    ) -> ResultList:
        user_pk = 1 if user.user_permission.is_anonymous() else user.id  # TODO: 비회원 처리
        data = (
            session.query(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .filter(Place.user_id == user_pk)
        )
        if tags:
            data = data.filter(Tag.id.in_(list(map(int, tags.split(",")))))
        return PlaceSerializer(
            data=data.order_by(Place.id, Tag.id).all()
        ).serialize()

    def _create_place(
        self, user: AuthUser, body: PlaceRegisterBody, session: Session
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
            session.flush()
        except IntegrityError as e:
            logger.error(f"장소 등록 실패 - body=({body}) error={e}")
            raise APIException(Http5XX.UNKNOWN_ERROR)
        return place

    def _create_tag(self, tag_ids: list, place_id: int, session: Session):
        if session.query(Tag).filter(Tag.id.in_(tag_ids)).count() != len(tag_ids):
            raise APIException(Http4XX.TAG_NOT_FOUND)
        for tag_id in tag_ids:
            place_tag = PlaceTag(place_id=place_id, tag_id=tag_id)
            session.add(place_tag)
        session.flush()

    def register(
        self, user: AuthUser, body: PlaceRegisterBody, session: Session
    ) -> ResultDict:
        place = self._create_place(user, body, session)
        if body.tag_ids:
            self._create_tag(body.tag_ids, place.id, session)
        result = self.get_place(user, place.id, session)
        session.commit()
        return result
