from fastapi import APIRouter

from .status import manager

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
def healthcheck() -> str:
    return "ok"


@router.get("/status", include_in_schema=False)
async def status() -> dict:
    return await manager.check()
