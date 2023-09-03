from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from app.common.models import Base


class Share(Base):
    __tablename__ = "t_share"

    id = Column(Integer, primary_key=True)
    key = Column(
        String(50), comment="공유된 컨텐츠들을 구분하는 문자열", nullable=False, unique=True
    )
    user_id = Column(Integer, ForeignKey("t_auth_user.id", ondelete="CASCADE"))
    description = Column(Text, comment="공유된 맛집들에 대한 설명", nullable=True)
    lat = Column(Float, comment="공유 시작할 위도", nullable=False)
    lng = Column(Float, comment="공유 시작할 경도", nullable=False)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )


class ShareLocation(Base):
    __tablename__ = "t_share_location"
    __table_args__ = (UniqueConstraint("share_id", "location_id"),)

    id = Column(Integer, primary_key=True)
    share_id = Column(Integer, ForeignKey("t_share.id", ondelete="CASCADE"))
    location_id = Column(
        Integer, ForeignKey("t_location.id", ondelete="CASCADE")
    )
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
