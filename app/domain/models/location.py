from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from app.common.models import Base


class Location(Base):
    __tablename__ = "t_location"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("t_auth_user.id", ondelete="CASCADE"))
    location_name = Column(String(30), comment="장소 이름", nullable=False)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )


class PlaceLocation(Base):
    __tablename__ = "t_place_location"
    __table_args__ = (UniqueConstraint("place_id", "location_id"),)

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey("t_place.id", ondelete="CASCADE"))
    location_id = Column(
        Integer, ForeignKey("t_location.id", ondelete="CASCADE")
    )
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
