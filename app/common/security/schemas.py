from enum import Enum

from pydantic import BaseModel, PositiveInt


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def is_access_token(self) -> bool:
        return self.value == "access"

    def is_refresh_token(self) -> bool:
        return self.value == "refresh"


class CredentialPayload(BaseModel):
    type: TokenType
    pk: PositiveInt
    permission: str
    user_name: str
    exp: int
    iat: int


class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    token: str
    payload: CredentialPayload
