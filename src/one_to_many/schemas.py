from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str


class BookOut(BaseModel):
    title: str
    id: UUID


class BookEdit(BaseModel):
    title: Optional[str]


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str

    books: Optional[list[BookCreate]]


class AuthorRead(BaseModel):
    id: UUID


class AuthorOut(AuthorCreate):
    books: Optional[list[BookOut]]

    model_config = ConfigDict(from_attributes=True)


class AuthorEdit(AuthorCreate):
    pass