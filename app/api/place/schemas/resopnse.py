from datetime import datetime
from typing import TypedDict

from app.common.schemas import SuccessResponse


class Tag(TypedDict):
    id: int
    tag_name: str
    memo: str
    create_dtm: datetime


class Place(TypedDict):
    id: int
    place_name: str
    description: str
    lat: float
    lng: float
    address: str
    created_dtm: datetime
    tags: list[Tag]


class PlaceResponse(SuccessResponse):
    """장소 응답"""

    data: Place


class PlaceListResponse(SuccessResponse):
    """장소 리스트 응답"""

    data: list[Place]


class TagResponse(SuccessResponse):
    """태그 응답"""

    data: Tag


class TagListResponse(SuccessResponse):
    """태그 리스트 응답"""

    data: list[Tag]
