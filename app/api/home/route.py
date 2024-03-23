from fastapi import APIRouter, Depends

from app.config.settings import get_settings
from app.config.settings.base import Settings
from .status import manager

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
def healthcheck() -> str:
    return "ok"


@router.get("/status", include_in_schema=False)
async def healthcheck(settings: Settings = Depends(get_settings)) -> dict:
    return await manager.check()
