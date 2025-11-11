from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str


class BookOut(BaseModel):
    title: str
    author_id: UUID


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str

    books: Optional[list[BookCreate]]


class AuthorRead(BaseModel):
    id: UUID


class AuthorOut(AuthorCreate):
    id: UUID