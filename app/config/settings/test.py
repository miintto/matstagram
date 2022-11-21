from .base import LOG_DIR, Settings


class TestSettings(Settings):
    APP_ENV = "test"
    DEBUG: bool = True

    SECRET_KEY = "test"

    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s"
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
                "formatter": "default",
                "filename": f"{LOG_DIR}/api.log",
            },
        },
        "loggers": {
            "fastapi.request": {
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "app": {
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    DB_NAME = "test_db"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5432

    SQLALCHEMY_POOL_SIZE = 10
