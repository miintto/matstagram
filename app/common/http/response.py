from typing import Any

from fastapi.responses import JSONResponse

from .codes import BaseHttp


class APIResponse(JSONResponse):
    def __init__(self, code: BaseHttp, data: Any = None, **kwargs) -> None:
        super().__init__(
            content={
                "code": code.code,
                "message": code.message,
                "data": data,
            },
            status_code=code.status_code,
            **kwargs,
        )
