from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.models import AuthUser
from app.common.exception import APIException
from app.common.response.codes import Http4XX
from app.common.types import ResultDict, ResultList
from ..models import Tag
from ..schemas.request import TagBody


class TagHandler:
    @staticmethod
    async def get_user_tag_list(
        user: AuthUser, session: AsyncSession
    ) -> ResultList:
        user_pk = 1 if user.user_permission.is_anonymous() else user.id  # TODO: 비회원 처리
        result = await session.execute(
            select(Tag).where(Tag.user_id == user_pk)
        )
        return [tag.to_dict() for tag in result.scalars()]

    async def create(
        self, user: AuthUser, body: TagBody, session: AsyncSession
    ) -> ResultDict:
        tag = Tag(user_id=user.id, tag_name=body.tag_name, memo=body.memo)
        session.add(tag)
        result = tag.to_dict()
        await session.commit()
        return result

    async def update(
        self, user_pk: int, tag_id: int, body: TagBody, session: AsyncSession
    ) -> ResultDict:
        try:
            result = await session.execute(
                select(Tag).where(Tag.id == tag_id, Tag.user_id == user_pk)
            )
            tag = result.scalar_one()
        except NoResultFound:
            raise APIException(Http4XX.TAG_NOT_FOUND)
        tag.tag_name = body.tag_name
        tag.memo = body.memo
        result = tag.to_dict
        await session.commit()
        return result
