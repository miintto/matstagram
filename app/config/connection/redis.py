from redis.asyncio import Redis

from app.config.settings import get_settings

settings = get_settings()


class RedisConnection:
    def __init__(self):
        self._conn = None

    def init_app(self):
        self._conn = Redis.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )

    @property
    def connection(self) -> Redis:
        return self._conn

    async def ping(self):
        await self._conn.ping()

    async def close_connection(self):
        await self._conn.close()
