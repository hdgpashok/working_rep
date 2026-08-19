import uuid

from src.models.authors import AuthorModel
from src.models.books import BookModel


class AuthorMapping:
    @staticmethod
    def dict_to_author_model(data: dict) -> AuthorModel:
        author_id = uuid.UUID(data["id"])

        books = [
            BookModel(
                id=uuid.UUID(book["id"]),
                title=book["title"],
                author_id=author_id,
            )
            for book in data.get("books", [])
        ]

        return AuthorModel(
            id=author_id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            books=books,
        )