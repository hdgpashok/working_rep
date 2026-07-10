from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from src.exceptions.base import AppException


class CacheError(AppException):
    def __init__(self, message: str = "Cache service error"):
        super().__init__(
            message=message,
            status_code=HTTP_503_SERVICE_UNAVAILABLE
        )