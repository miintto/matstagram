from asyncio import current_task
import logging

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class DBConnection:
    def __init__(self) -> None:
        self.engine = None
        self._session = None

    def create_session(self) -> AsyncEngine:
        return create_async_engine(
            url="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                name=settings.DB_NAME,
            ),
            pool_size=settings.SQLALCHEMY_POOL_SIZE,
        )

    def init_app(self):
        self.engine = self.create_session()
        self._session = async_scoped_session(
            session_factory=async_sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

    async def dispose_connection(self):
        await self.engine.dispose()

    async def get_session(self) -> AsyncSession:
        async with self._session() as session:
            try:
                yield session
            finally:
                await session.close()
        await self._session.remove()

    @property
    def session(self):
        return self.get_session
