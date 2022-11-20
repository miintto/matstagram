from datetime import datetime
from typing import TypedDict

from app.common.schemas import CreatedResponse, SuccessResponse


class Tag(TypedDict):
    id: int
    tag_name: str
    memo: str | None
    created_dtm: datetime


class Place(TypedDict):
    id: int
    place_name: str
    description: str | None
    lat: float
    lng: float
    address: str | None
    created_dtm: datetime
    tags: list[Tag]


class PlaceResponse(SuccessResponse):
    """장소 응답"""

    data: Place


class PlaceCreatedResponse(CreatedResponse):
    """태그 등록 응답"""

    data: Place


class PlaceListResponse(SuccessResponse):
    """장소 리스트 응답"""

    data: list[Place]


class TagResponse(SuccessResponse):
    """태그 응답"""

    data: Tag


class TagCreatedResponse(CreatedResponse):
    """태그 생성 응답"""

    data: Tag


class TagListResponse(SuccessResponse):
    """태그 리스트 응답"""

    data: list[Tag]
