from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.common.models import Base


class Tag(Base):
    __tablename__ = "t_tag"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("t_auth_user.id", ondelete="CASCADE"))
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
            "created_dtm": self.created_dtm.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }


class PlaceTag(Base):
    __tablename__ = "t_place_tag"

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey("t_place.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("t_tag.id", ondelete="CASCADE"))
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
