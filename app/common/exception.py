from app.common.http.codes import BaseHttp


class APIException(Exception):
    def __init__(self, error: BaseHttp, **kwargs) -> None:
        self.error = error
        self.extra = kwargs
        super().__init__(error.message)
