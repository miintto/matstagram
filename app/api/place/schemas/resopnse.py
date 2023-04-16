from datetime import datetime

from pydantic import BaseModel, Field

from app.common.schemas import CreatedResponse, SuccessResponse


class Tag(BaseModel):
    id: int = Field(title="Primary Key", description="태그 pk", example=37)
    tag_name: str = Field(title="태그명", example="망원동맛짐")
    memo: str | None = Field(
        title="메모",
        description="태그에 대한 간략한 설멍",
        example="망원동에 있는 맛집들",
    )
    created_dtm: datetime = Field(
        title="태그 생성 일시",
        pattern="YYYY-MM-DD HH:Mi:SS.ffffff",
        example="2021-03-22 19:32:14.281734",
    )


class Place(BaseModel):
    id: int = Field(title="Primary Key", description="맛집 pk", example=21)
    place_name: str = Field(title="식당 이름", example="소금집델리")
    description: str | None = Field(title="맛집 설명", example="잠봉뵈르 샌드위치 존맛탱~")
    lat: float = Field(
        title="위도",
        description="맛집이 위치한 위도 좌표",
        example=37.556808,
    )
    lng: float = Field(
        title="경도",
        description="맛집이 위치한 경도 좌표",
        example=126.908262,
    )
    address: str | None = Field(
        title="맛집 주소",
        description="해당 식당이 위치한 상세 주소",
    )
    image_url: str | None = Field(
        title="맛집 대표 이미지",
        description="맛집을 설명할 수 있는 이미지 url",
    )
    created_dtm: datetime = Field(
        title="맛집 등록 일시",
        pattern="YYYY-MM-DD HH:Mi:SS.ffffff",
        example="2021-08-18 20:07:43.129340",
    )
    tags: list[Tag] = Field(title="맛집에 등록 태그 리스트")


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
