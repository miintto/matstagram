from enum import Enum
from typing import Any

from fastapi.responses import JSONResponse


class APIResponse(JSONResponse):
    def __init__(self, code: Enum, data: Any = None, **kwargs) -> None:
        super().__init__(
            content={
                "code": code.value[0],
                "message": code.value[1],
                "data": data,
            },
            status_code=code.value[2],
            **kwargs,
        )
