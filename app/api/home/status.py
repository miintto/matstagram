import asyncio
from enum import Enum
import logging
import platform
from typing import Coroutine

from fastapi import __version__ as fastapi_version

from app.config.settings import get_settings
from app.config.connection import db, redis

settings = get_settings()

logger = logging.getLogger(__name__)


class Service(Enum):
    postgres = db.check_connection()
    redis = redis.ping()


class StatusManager:
    @staticmethod
    async def _check_status(key: str, coroutine: Coroutine) -> tuple[str, str]:
        try:
            await coroutine
            return key, "ok"
        except Exception as e:
            logger.critical(f"Connection Error: {key} - {e}")
            return key, "fail"

    async def _collect_status(self) -> dict:
        tasks = (self._check_status(svc.name, svc.value) for svc in Service)
        return {key: status for key, status in await asyncio.gather(*tasks)}

    async def check(self) -> dict:
        return {"status": "ok"} | await self._collect_status() | {
            "env": settings.APP_ENV,
            "python": platform.python_version(),
            "fastapi": fastapi_version,
        }


manager = StatusManager()
