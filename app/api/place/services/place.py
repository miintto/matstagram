from sqlalchemy.orm import Session

from app.api.user.models import AuthUser, UserPermission
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.types import ResultDict, ResultList
from ..models import Place, PlaceTag, Tag
from ..schemas import PlaceRegisterBody
from ..serializers import PlaceSerializer


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

    def get_place_list(self, user: AuthUser, session: Session) -> ResultList:
        if user.user_permission == UserPermission.anonymous:  # TODO: 비회원 처리
            user_pk = 1
        else:
            user_pk = user.id
        data = (
            session.query(Place, Tag)
            .join(PlaceTag, Place.id == PlaceTag.place_id, isouter=True)
            .join(Tag, Tag.id == PlaceTag.tag_id, isouter=True)
            .filter(Place.user_id == user_pk)
            .order_by(Place.id, Tag.id)
            .all()
        )
        return PlaceSerializer(data).serialize()

    def _create_place_bucket(
        self, user: AuthUser, body: PlaceRegisterBody, session: Session
    ) -> Place:
        place = Place(
            user_id=user.id,
            place_name=body.place_name,
            description=body.description,
            lat=body.lat,
            lng=body.lng,
        )
        session.add(place)
        session.flush()
        return place

    def _create_tag(self, tag_ids: list, place_id: int, session: Session):
        for tag_id in tag_ids:
            if not session.query(Tag).filter(Tag.id == tag_id).first():
                raise APIException(Http4XX.TAG_NOT_FOUND)
            place_tag = PlaceTag(place_id=place_id, tag_id=tag_id)
            session.add(place_tag)

    def register(
        self, user: AuthUser, body: PlaceRegisterBody, session: Session
    ):
        place = self._create_place_bucket(user, body, session)
        if body.tag_ids:
            self._create_tag(body.tag_ids, place.id, session)
        session.commit()
