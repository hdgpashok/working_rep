from uuid import UUID

from src.exceptions.base import AppException


class ActorNotFound(AppException):
    def __init__(self, actor_id: UUID):
        super().__init__(
            message=f"Actor {actor_id} not found",
            status_code=404
        )