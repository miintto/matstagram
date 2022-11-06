import platform

from fastapi import __version__ as fastapi_version, APIRouter, Depends
from uvicorn import __version__ as uvicorn_version

from app import __version__ as application_version
from app.config.settings import get_settings
from app.config.settings.base import Settings

router = APIRouter()


@router.get("/healthcheck", include_in_schema=False)
def healthcheck(settings: Settings = Depends(get_settings)) -> dict:
    version = {
        "python": platform.python_version(),
        "fastapi": fastapi_version,
        "uvicorn": uvicorn_version,
        "application": application_version,
    }
    return {"status": "ok", "env": settings.APP_ENV, "version": version}
