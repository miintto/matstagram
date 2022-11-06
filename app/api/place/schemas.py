from pydantic import BaseModel


class PlaceRegisterBody(BaseModel):
    place_name: str
    description: str | None
    lat: float
    lng: float
    tag_ids: list | None


class TagBody(BaseModel):
    tag_name: str
    memo: str | None
