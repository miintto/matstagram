from fastapi.openapi.models import HTTPBearer
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from starlette.requests import Request

from app.common.exception import APIException
from app.common.response.codes import Http4XX
from .jwt import JWTHandler
from .schemas import HTTPAuthorizationCredentials


class Authentication(SecurityBase):
    """헤더에 있는 인증 정보를 가져와 유효성을 평가합니다.

    요청시 헤더에 인증 토큰을 추가하여 인증할 수 있습니다.
        "Authorization": "JWT {token}"
    """

    scheme = "JWT"

    def __init__(
        self,
        *,
        bearerFormat: str = None,
        description: str = None,
    ) -> None:
        self.model = HTTPBearer(
            bearerFormat=bearerFormat, description=description
        )
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.upper() != self.scheme:
            raise APIException(Http4XX.UNAUTHENTICATED)
        return self.decode_token(scheme, token)

    @staticmethod
    def decode_token(scheme: str, token: str) -> HTTPAuthorizationCredentials:
        try:
            credentials = HTTPAuthorizationCredentials(
                scheme=scheme,
                token=token,
                payload=JWTHandler().decode_token(token),
            )
        except ValidationError:
            raise APIException(
                Http4XX.UNAUTHENTICATED,
                data=f"인증 토큰 형식이 변형되었습니다. 다시 로그인 해주세요.",
            )
        if not credentials.payload.type.is_access_token():
            raise APIException(
                Http4XX.UNAUTHENTICATED,
                data=f"잘못된 인증 토큰입니다.: {credentials.payload.type}",
            )
        return credentials
