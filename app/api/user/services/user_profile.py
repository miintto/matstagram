from sqlalchemy.orm import Session

from app.common.exception import APIException
from app.common.response.codes import Http4XX
from ..models import AuthUser
from ..schemas.request import NewPasswordBody, UserInfoBody


class UserProfile:
    def _validate_user_name(self, user_name: str, session: Session) -> bool:
        if session.query(AuthUser).filter(
            AuthUser.user_name == user_name
        ).first():
            raise APIException(Http4XX.DUPLICATED_USER_NAME, data=user_name)
        return True

    def _validate_user_email(self, user_email: str, session: Session) -> bool:
        if session.query(AuthUser).filter(
            AuthUser.user_email == user_email
        ).first():
            raise APIException(Http4XX.DUPLICATED_USER_EMAIL, data=user_email)
        return True

    def update(
        self, user: AuthUser, body: UserInfoBody, session: Session
    ) -> dict:
        if self._validate_user_name(body.user_name, session):
            user.user_name = body.user_name
        if self._validate_user_email(body.user_email, session):
            user.user_email = body.user_email
        session.commit()
        return user.to_dict()

    def change_image(
        self, user: AuthUser, profile_image: str, session: Session
    ) -> dict:
        user.profile_image = profile_image
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

