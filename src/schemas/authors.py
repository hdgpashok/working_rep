from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.books import BookCreate, BookOut, BookUpdate


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorRead(BaseModel):
    id: UUID


class AuthorCreate(AuthorBase):
    books: list[BookCreate]


class AuthorOut(AuthorBase):
    id: UUID
    books: list[BookOut]

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(AuthorBase):
    books: list[BookUpdate]