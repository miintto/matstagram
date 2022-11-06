import logging
import uuid

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("fastapi.request")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        key = str(uuid.uuid4())[:5]
        log_msg = f"[{key}] - {request.method} {request.url.path}"
        logger.info(log_msg)
        response = await call_next(request)
        logger.info(f"{log_msg} - {response.status_code}")
        return response
