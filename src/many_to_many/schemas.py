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
    theatres: Optional[list[TheatreCreate]] = None


class ActorRead(ActorBase):
    pass


class ActorOut(ActorBase):
    theatres: Optional[list[TheatreOut]]


class ActorUpdate(ActorBase):
    theatres: Optional[list[TheatreCreate]] = None


class ActorDelete(ActorRead):
    pass
