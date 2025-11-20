from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TheatreBase(BaseModel):
    name: str
    address: str


class TheatreRead(TheatreBase):
    pass


class TheatreOut(TheatreBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TheatreCreate(TheatreBase):
    pass


class TheatreUpdate(TheatreBase):
    pass


class TheatreDelete(TheatreRead):
    pass


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    theatres: list[TheatreCreate]


class ActorRead(ActorBase):
    pass


class ActorOut(ActorBase):
    theatres: list[TheatreOut]

    model_config = ConfigDict(from_attributes=True)


class ActorUpdate(ActorBase):
    theatres: list[TheatreCreate]


class ActorDelete(ActorRead):
    pass
