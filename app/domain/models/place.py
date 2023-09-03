from datetime import datetime
import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.common.models import Base


class PlaceType(enum.Enum):
    restaurant = "restaurant"  # 맛집
    tourist_spot = "tourist_spot"  # 관광 명소
    accommodation = "accommodation"  # 숙소


class Place(Base):
    """장소"""
    __tablename__ = "t_place"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("t_auth_user.id", ondelete="CASCADE"))
    place_name = Column(
        String(60), comment="장소 이름", nullable=False, unique=True
    )
    description = Column(Text, comment="소개글", nullable=True)
    lat = Column(Float, comment="위도", nullable=True)
    lng = Column(Float, comment="경도", nullable=True)
    address = Column(String(254), comment="상세 주소", nullable=True)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    image_url = Column(Text, comment="대표 이미지 url", nullable=True)
    place_type = Column(
        Enum(PlaceType, native_enum=False, length=30),
        comment="장소 유형",
        nullable=False,
        default=PlaceType.restaurant,
    )
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
            "image_url": self.image_url,
            "created_dtm": self.created_dtm.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }
