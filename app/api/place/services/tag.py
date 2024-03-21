from fastapi import Depends
from sqlalchemy.exc import NoResultFound

from app.common.exception import APIException
from app.common.http.codes import Http4XX
from app.common.types import ResultDict, ResultList
from app.domain.models.tag import Tag
from app.domain.models.user import AuthUser
from app.domain.repository.tag import TagRepository
from ..schemas.request import TagBody


class TagService:
    def __init__(self, tag_repository: TagRepository = Depends(TagRepository)):
        self.tag_repository = tag_repository

    async def get_user_tag_list(self, user: AuthUser) -> ResultList:
        user_id = 1 if user.user_permission.is_anonymous() else user.id  # TODO: 비회원 처리
        return [
            tag.to_dict()
            for tag
            in await self.tag_repository.get_tag_list_by_user(user_id)
        ]

    async def create(self, user: AuthUser, body: TagBody) -> ResultDict:
        tag = Tag(user_id=user.id, tag_name=body.tag_name, memo=body.memo)
        await self.tag_repository.save(tag)
        return tag.to_dict()

    async def update(
        self, user_pk: int, tag_id: int, body: TagBody
    ) -> ResultDict:
        try:
            tag = await self.tag_repository.get_tag_by_id(tag_id)
            assert tag.user_id == user_pk
        except NoResultFound:
            raise APIException(Http4XX.TAG_NOT_FOUND)
        tag.tag_name = body.tag_name
        tag.memo = body.memo
        await self.tag_repository.save(tag)
        return tag.to_dict()
