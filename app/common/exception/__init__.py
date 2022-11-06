from enum import Enum


class APIException(Exception):
    def __init__(self, error: Enum, **kwargs) -> None:
        self.error = error
        self.extra = kwargs
        super().__init__(error.value[1])
