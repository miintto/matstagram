from sqlalchemy.orm import Session

from app.common.exception import APIException
from app.common.response.codes import Http4XX
from ..models import AuthUser
from ..schemas.request import NewPasswordBody, UserInfoBody


class UserProfile:
    def _validate_user_name(
        self, user_name: str, user_pk: int, session: Session
    ) -> bool:
        if session.query(AuthUser).filter(
            AuthUser.user_name == user_name, AuthUser.id != user_pk
        ).first():
            raise APIException(Http4XX.DUPLICATED_USER_NAME, data=user_name)
        return True

    def _validate_user_email(
        self, user_email: str, user_pk: int, session: Session
    ) -> bool:
        if session.query(AuthUser).filter(
            AuthUser.user_email == user_email, AuthUser.id != user_pk
        ).first():
            raise APIException(Http4XX.DUPLICATED_USER_EMAIL, data=user_email)
        return True

    async def update(
        self, user: AuthUser, body: UserInfoBody, session: Session
    ) -> dict:
        self._validate_user_name(body.user_name, user.id, session)
        self._validate_user_email(body.user_email, user.id, session)
        user.user_name = body.user_name
        user.user_email = body.user_email
        if body.profile_image:
            user.profile_image = body.profile_image
        session.commit()
        return user.to_dict()

    def change_password(
        self, user: AuthUser, body: NewPasswordBody, session: Session
    ) -> bool:
        if not user.check_password(body.password):
            raise APIException(Http4XX.INVALID_PASSWORD)
        if body.new_password != body.new_password_check:
            raise APIException(Http4XX.MISMATCHED_PASSWORD)
        user.set_password(body.new_password)
        session.commit()
        return True
