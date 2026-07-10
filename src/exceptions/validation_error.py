from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from src.exceptions.base import AppException


class ValidationError(AppException):
    def __init__(self, message: str = "Data validation error"):
        super().__init__(
            message=message,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )