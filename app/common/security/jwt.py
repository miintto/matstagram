from datetime import datetime, timedelta
import jwt
import time

from app.common.exception import APIException
from app.common.http.codes import Http4XX
from app.config.settings import get_settings
from app.domain.models.user import AuthUser
from .schemas import TokenType


class JWTHandler:

    ALGORITHM = "HS256"
    JWT_ACCESS_EXPIRATION_INTERVAL = timedelta(days=365)
    JWT_REFRESH_EXPIRATION_INTERVAL = timedelta(days=90)
    JWT_SECRET_KEY = get_settings().SECRET_KEY

    def _encode_token(self, exp_interval: timedelta, **kwargs) -> str:
        now = datetime.now()
        kwargs["exp"] = int(time.mktime((now + exp_interval).timetuple()))
        kwargs["iat"] = int(time.mktime(now.timetuple()))
        return jwt.encode(
            payload=kwargs, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def generate_access_token(self, user: AuthUser) -> str:
        return self._encode_token(
            exp_interval=self.JWT_ACCESS_EXPIRATION_INTERVAL,
            type=TokenType.ACCESS.value,
            pk=user.id,
            permission=user.user_permission.name,
            user_name=user.user_name,
        )

    def generate_refresh_token(self, user: AuthUser) -> str:
        return self._encode_token(
            exp_interval=self.JWT_REFRESH_EXPIRATION_INTERVAL,
            type=TokenType.REFRESH.value,
            pk=user.id,
            is_active=user.is_active,
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token, key=self.JWT_SECRET_KEY, algorithms=self.ALGORITHM
            )
        except jwt.DecodeError:
            raise APIException(Http4XX.UNAUTHENTICATED, data="토큰 Decoding 에러.")
        except jwt.ExpiredSignatureError:
            raise APIException(Http4XX.UNAUTHENTICATED, data="만료된 토큰입니다.")
        except jwt.InvalidTokenError:
            raise APIException(Http4XX.UNAUTHENTICATED)
