from .base import LOG_DIR, Settings


class ProdSettings(Settings):
    DEBUG: bool = False

    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s"
            },
            "ecs": {
                "()": "ecs_logging.StdlibFormatter",
                "exclude_fields": ["log.original"],
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "ecs",
                "filename": f"{LOG_DIR}/api.log",
            },
        },
        "loggers": {
            "fastapi.request": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "app": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    class Config:
        env_file = (".env.production", ".env")
