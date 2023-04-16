from pydantic import BaseModel, Field

from app.common.schemas import CreatedResponse


class ShareBody(BaseModel):
    description: str = Field(title="공유할 맛집에 대한 설명")
    lat: float = Field(title="공유 시작할 위도", example=37.54)
    lng: float = Field(title="공유 시작할 경도", example=127.12)
    locations: list[int] = Field(title="공유할 지역 pk 리스트", example=[37, 38, 40])


class ShareCreatedResponse(CreatedResponse):
    data: str = Field(
        title="공유 데이터 생성 후 매칭되는 key 값", example="f81cdd232b484e9aac36"
    )
