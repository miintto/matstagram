import os
from functools import lru_cache
import inspect
from importlib import import_module

from app.config.settings.base import Settings
from tests.management.utils import is_test


__all__ = ["get_settings"]


@lru_cache()
def get_settings() -> Settings:
    env = os.environ.get("APP_ENV", "local") if not is_test() else "test"
    for _, _settings in (
        import_module(f".{env}", "app.config.settings").__dict__.items()
    ):
        if (
            inspect.isclass(_settings)
            and issubclass(_settings, Settings)
            and _settings != Settings
        ):
            return _settings()
