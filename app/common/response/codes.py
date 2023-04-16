from enum import Enum

from starlette import status


class Http2XX(Enum):
    SUCCESS = ("S000", "성공", status.HTTP_200_OK)
    CREATED = ("S001", "생성 완료", status.HTTP_201_CREATED)


class Http4XX(Enum):
    BAD_REQUEST = ("F000", "잘못된 요청입니다.", status.HTTP_400_BAD_REQUEST)
    UNAUTHENTICATED = ("F001", "잘못된 인증 정보입니다.", status.HTTP_401_UNAUTHORIZED)
    PERMISSION_DENIED = ("F002", "권한이 없습니다.", status.HTTP_403_FORBIDDEN)
    USER_NOT_FOUND = ("F003", "계정이 존재하지 않습니다.", status.HTTP_404_NOT_FOUND)
    INVALID_PASSWORD = (
        "F004", "비밀번호가 일치하지 않습니다.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    PLACE_NOT_FOUND = ("F005", "장소를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
    TAG_NOT_FOUND = ("F006", "태그를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)
    DUPLICATED_USER_NAME = (
        "F007", "중복된 닉네임입니다.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    DUPLICATED_USER_EMAIL = (
        "F008", "중복된 이메일입니다.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    MISMATCHED_PASSWORD = (
        "F009", "동일한 비밀번호를 입력하세요.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    INVALID_FILE_FORMAT = (
        "F010", "올바르지 않은 형식의 파일입니다.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    SHARE_NOT_FOUND = ("F011", "공유된 장소를 찾을 수 없습니다.", status.HTTP_404_NOT_FOUND)


class Http5XX(Enum):
    UNKNOWN_ERROR = (
        "E000", "알 수 없는 에러 발생", status.HTTP_500_INTERNAL_SERVER_ERROR
    )
