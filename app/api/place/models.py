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
)

from app.common.models import Base


class Place(Base):
    """장소"""
    __tablename__ = "t_place"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("t_auth_user.id"))
    place_name = Column(
        String(60), comment="장소 이름", nullable=False, unique=True
    )
    description = Column(Text, comment="소개글", nullable=True)
    lat = Column(Float, comment="위도", nullable=True)
    lng = Column(Float, comment="경도", nullable=True)
    address = Column(String(254), comment="상세 주소", nullable=True)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "place_name": self.place_name,
            "description": self.description,
            "lat": self.lat,
            "lng": self.lng,
            "address": self.address,
            "created_dtm": self.created_dtm.strftime("%Y-%m-%d %H:%H:%S.%f"),
        }


class Tag(Base):
    __tablename__ = "t_tag"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("t_auth_user.id"))
    tag_name = Column(String(30), comment="태그 이름", nullable=False)
    memo = Column(Text, comment="메모", nullable=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "tag_name": self.tag_name,
            "memo": self.memo,
            "created_dtm": self.created_dtm.strftime("%Y-%m-%d %H:%H:%S.%f"),
        }


class PlaceTag(Base):
    __tablename__ = "t_place_tag"

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey("t_place.id"))
    tag_id = Column(Integer, ForeignKey("t_tag.id"))
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
