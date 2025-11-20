from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Mapped, mapped_column


class BookBase(BaseModel):
    title: str


class BookRead(BaseModel):
    id: Mapped[UUID]


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class BookEdit(BookBase):
    pass


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorRead(BaseModel):
    id: UUID


class AuthorCreate(AuthorBase):
    books: list[BookCreate]


class AuthorOut(AuthorBase):
    books: list[BookOut]

    model_config = ConfigDict(from_attributes=True)


class AuthorEdit(AuthorBase):
    pass