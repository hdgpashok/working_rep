from uuid import UUID

from fastapi import status

from src.exceptions.base import AppException


class UserNotFound(AppException):
    def __init__(self, user_id: UUID):
        super().__init__(
            message=f"User {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )