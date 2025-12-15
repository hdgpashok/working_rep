from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str


class BookRead(BaseModel):
    id: UUID


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BookBase):
    pass