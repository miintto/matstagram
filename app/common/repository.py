from abc import ABC

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.connection import db


class BaseRepository(ABC):
    """Database CRUD 인터페이스"""

    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session

    async def save(self, instance, refresh: bool = False):
        self._session.add(instance)
        await self._session.commit()
        if refresh:
            await self._session.refresh(instance)
            return instance
