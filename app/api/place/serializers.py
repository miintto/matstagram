from typing import Sequence

from sqlalchemy.engine.row import Row

from app.common.types import ResultList
from app.domain.models.place import Place


class PlaceSerializer:
    def __init__(self, data: Sequence[Row]):
        self.data = data
        self.place_id = -1
        self.tag_list = []

    def _initialize(self, place_id):
        self.place_id = place_id
        self.tag_list = []

    def serialize_place(self, place: Place):
        self._initialize(place.id)
        data = place.to_dict()
        data["tags"] = self.tag_list
        return data

    def serialize(self) -> ResultList:
        result_list = []
        for row in self.data:
            if self.place_id != row.Place.id:
                result_list.append(self.serialize_place(row.Place))
            if not row.Tag:
                continue
            self.tag_list.append(row.Tag.to_dict())
        return result_list
