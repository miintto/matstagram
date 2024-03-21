import logging

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from app.common.http.codes import Http4XX, Http5XX
from app.common.http.response import APIResponse
from app.common.exception import APIException

logger = logging.getLogger(__name__)


async def api_exception_handler(
    request: Request, exc: APIException
) -> APIResponse:
    logger.error(f"APIException - {exc}")
    return APIResponse(exc.error, data=exc.extra.get("data"))


async def request_validation_exception_error_handler(
    request: Request, exc: RequestValidationError
) -> APIResponse:
    logger.error(f"RequestValidationError - {exc}")
    return APIResponse(Http4XX.BAD_REQUEST, data=exc.errors())


async def default_exception_handler(
    request: Request, exc: Exception
) -> APIResponse:
    logger.exception(f"Exception - {exc}")
    return APIResponse(Http5XX.UNKNOWN_ERROR, data=exc.args)


exception_handlers = {
    APIException: api_exception_handler,
    RequestValidationError: request_validation_exception_error_handler,
    Exception: default_exception_handler,
}
