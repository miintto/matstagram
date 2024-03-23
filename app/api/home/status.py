import asyncio
import logging
import platform
import socket

from fastapi import __version__ as fastapi_version

from app.config.settings import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


class StatusManager:
    @staticmethod
    async def check_postgresql() -> bool:
        try:
            await asyncio.wait_for(
                asyncio.open_connection(
                    settings.DB_HOST, settings.DB_PORT, limit=1
                ),
                timeout=1
            )
            return True
        except asyncio.TimeoutError:
            return False
        except Exception as e:
            logger.critical(f"PostgreSQL Connection Error! - {e}")
            return False

    async def check(self) -> dict:
        return {
            "status": "ok",
            "postgres": "ok" if await self.check_postgresql() else "fail",
            "env": settings.APP_ENV,
            "python": platform.python_version(),
            "fastapi": fastapi_version,
        }


manager = StatusManager()
