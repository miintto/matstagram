import logging
import uuid

from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("fastapi.request")


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        log_msg = self.make_logging_message(scope)
        logger.info(log_msg)

        async def logging_response_after_send(message: Message):
            nonlocal log_msg

            await send(message)

            if message["type"] == "http.response.start":
                logger.info(f"{log_msg} - {message['status']}")

        await self.app(scope, receive, logging_response_after_send)

    def make_logging_message(self, scope: Scope) -> str:
        """`[abcde] - GET /path?key=value` 형태로 로깅되도록"""

        return "[{key}] - {methed} {path}{query}".format(
            key=str(uuid.uuid4())[:5],
            methed=scope.get('method'),
            path=scope.get('path'),
            query=(
                "?" + scope.get("query_string").decode("utf-8")
                if scope.get("query_string")
                else ""
            ),
        )
