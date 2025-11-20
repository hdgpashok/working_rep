from uuid import UUID

from src.exceptions.base import AppException


class AuthorNotFound(AppException):
    def __init__(self, author_id: UUID):
        super().__init__(
            message=f"Author {author_id} not found",
            status_code=404
        )