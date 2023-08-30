import asyncio
import os

from httpx import AsyncClient

from app.common.models import Base

os.environ.setdefault("APP_ENV", "test")


class BaseTestCase:
    @classmethod
    def setup_class(cls):
        from app.config.connection import db
        from app.main import app

        assert app.extra.get("env") == "test"

        cls.db = db
        cls.client = AsyncClient(app=app, base_url="http://test.nolbal.com")
        asyncio.run(cls()._create_table())

    @classmethod
    def teardown_class(cls):
        asyncio.run(cls()._drop_table())

    async def _create_table(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
        await self.db.engine.dispose()

    async def _drop_table(self):
        await self.db.engine.dispose()
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.commit()
        await self.db.engine.dispose()
