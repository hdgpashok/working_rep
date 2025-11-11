from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str

    books: Optional[list[BookCreate]]
