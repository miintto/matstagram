from fastapi import UploadFile

from .base import BaseUpload


class UploadProfileImage(BaseUpload):
    """사용자 프로필 이미지 저장"""

    def __init__(self):
        super().__init__()
        self.upload_to = "img/profile/"

    valid_content_type = ("image/jpeg", "image/png")

    def __call__(self, profile_image: UploadFile) -> str:
        return self.upload(
            file=profile_image,
            file_name=self.generate_file_name(profile_image.filename),
        )
