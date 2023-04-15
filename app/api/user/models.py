from datetime import datetime
import enum

import bcrypt
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.common.models import Base


class UserPermission(enum.Enum):
    anonymous = "anonymous"
    normal = "normal"
    admin = "admin"

    def is_anonymous(self):
        return self == self.anonymous

    def is_admin(self):
        return self == self.admin


class AuthUser(Base):
    __tablename__ = "t_auth_user"

    id = Column(Integer, primary_key=True)
    user_name = Column(
        String(30), comment="사용자 이름", nullable=False, unique=True
    )
    user_email = Column(
        String(254), comment="이메일", nullable=False, unique=True
    )
    password = Column(Text, comment="비밀번호", nullable=True)
    user_permission = Column(
        Enum(UserPermission, native_enum=False, length=15),
        comment="사용자 권한",
        nullable=False,
        default=UserPermission.normal,
    )
    profile_image = Column(Text, comment="사용자 프로필 이미지", nullable=True)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
    last_login_dtm = Column(DateTime, comment="마지막 로그인 일시", nullable=True)
    tags = relationship("Tag")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password.encode("utf-8")
        )

    def to_dict(self, load: bool = False) -> dict:
        data = {
            "id": self.id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "user_permission": self.user_permission.name,
            "profile_image": self.profile_image,
            "is_active": self.is_active,
            "created_dtm": self.created_dtm.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "last_login_dtm": (
                self.last_login_dtm.strftime("%Y-%m-%d %H:%M:%S.%f")
                if self.last_login_dtm
                else None
            ),
        }
        if load:
            data["tags"] = [tag.to_dict() for tag in self.tags]
        return data
