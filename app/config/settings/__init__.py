import os
from functools import lru_cache

from .base import Settings
from .local import LocalSettings
from .production import ProdSettings
from .test import TestSettings


__all__ = ["get_settings"]


_settings = {
    "local": LocalSettings,
    "production": ProdSettings,
    "test": TestSettings,
}


@lru_cache()
def get_settings() -> Settings:
    env = os.environ.get("APP_ENV", "local")
    print(f"APP_ENV:  {env}")
    return _settings[env]()
