import os
import uuid

from fastapi import UploadFile

from app.common.exception import APIException
from app.common.http.codes import Http4XX
from app.config.settings import get_settings

settings = get_settings()


class BaseUpload:

    valid_content_type = ()

    def __init__(self):
        self.static_dir = settings.STATIC_DIR
        self.upload_to = ""

    def upload(self, file: UploadFile, file_name: str) -> str:
        self.validate(file)
        file_path = os.path.join(self.static_dir, self.upload_to, file_name)
        with open(file_path, "wb+") as f:
            f.write(file.file.read())
        return os.path.join("/static/", self.upload_to, file_name)

    def validate(self, profile_image: UploadFile):
        if (
            self.valid_content_type
            and profile_image.content_type not in self.valid_content_type
        ):
            raise APIException(
                Http4XX.INVALID_FILE_FORMAT, data=profile_image.content_type
            )

    @staticmethod
    def generate_file_name(file_name: str) -> str:
        name, _, e = file_name.partition(".")
        return ".".join([f"{name}{str(uuid.uuid4())[-13:]}", e])
