from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.user.models import AuthUser
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.types import ResultDict, ResultList
from ..models import Tag
from ..schemas import TagBody


class TagHandler:
    @staticmethod
    def get_user_tag_list(user: AuthUser, session: Session) -> ResultList:
        user_pk = 1 if user.user_permission.is_anonymous() else user.id  # TODO: 비회원 처리
        tags = session.query(Tag).filter(Tag.user_id == user_pk).all()
        return [tag.to_dict() for tag in tags]

    def create(self, user: AuthUser, body: TagBody, session: Session) -> bool:
        tag = Tag(user_id=user.id, tag_name=body.tag_name, memo=body.memo)
        session.add(tag)
        session.commit()
        return True

    def update(
        self, user: AuthUser, tag_id: int, body: TagBody, session: Session
    ) -> ResultDict:
        try:
            tag = session.query(Tag).filter(
                Tag.id == tag_id, Tag.user_id == user.id
            ).one()
        except NoResultFound:
            raise APIException(Http4XX.TAG_NOT_FOUND)
        tag.tag_name = body.tag_name
        tag.memo = body.memo
        session.commit()
        return tag.to_dict()
