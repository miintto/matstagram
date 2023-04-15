from pydantic import BaseModel, Field


class PlaceRegisterBody(BaseModel):
    place_name: str = Field(
        title="식당 이름",
        example="소금집델리",
    )
    description: str | None = Field(
        title="맛집 설명",
        description="맛집에 대한 간단한 설명",
        example="잠봉뵈르 샌드위치 존맛탱~",
    )
    lat: float = Field(
        title="위도",
        description="입력할 맛집의 위도 좌표를 입력합니다.",
        example=37.556808,
    )
    lng: float = Field(
        title="경도",
        description="입력할 맛집의 경도 좌표를 입력합니다.",
        example=126.908262,
    )
    tag_ids: list[int] = Field(
        title="태그 리스트",
        description="등록할 태그의 pk 들을 입력합니다. 태그를 선택하지 않은 경우 빈 리스트(`[]`)를 입력합니다.",
        example=[37],
    )


class TagBody(BaseModel):
    tag_name: str = Field(
        title="태그명",
        description="앞에 \"#\"은 자동으로 붙어 노출되므로 되도록 기입하지 않도록 합니다.",
        example="망원동맛짐",
    )
    memo: str | None = Field(
        title="메모",
        description="태그에 대한 간략한 설멍",
        example="망원동에 있는 맛집들",
    )
