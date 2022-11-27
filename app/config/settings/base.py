import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = str(Path(__file__).parents[3])
LOG_DIR = os.path.join(BASE_DIR, "logs/")
STATIC_DIR = os.path.join(BASE_DIR, "static/")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


class Settings(BaseSettings):

    APP_ENV: str
    BASE_DIR: str = BASE_DIR
    DEBUG: str

    SECRET_KEY: str

    STATIC_DIR: str = STATIC_DIR

    LOG_DIR: str = LOG_DIR
    LOGGING_CONFIG: dict

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    SQLALCHEMY_POOL_SIZE: int

    class Config:
        env_file = ".env"
