import logging.config

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.staticfiles import StaticFiles

from app import __version__
from app.config.connection import db
from app.config.middleware.logging import LoggingMiddleware
from app.config.router import router
from app.config.settings import get_settings
from app.common.exception.handlers import exception_handlers

settings = get_settings()


def create_app():
    app = FastAPI(
        routes=router.routes,
        title="맛스타그램",
        description="지도에서 나만의 맛집을 추가하고 관리하자!",
        version=__version__,
        docs_url=None,
        redoc_url="/documents",
        middleware=[Middleware(LoggingMiddleware)],
        exception_handlers=exception_handlers,
        env=settings.APP_ENV,
    )

    # Databases
    db.init_app()
    app.router.add_event_handler("shutdown", db.dispose_connection)

    # Loggings
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # Static
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app
