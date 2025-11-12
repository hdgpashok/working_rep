from typing import Optional

from pydantic import BaseModel, ConfigDict


class TheatreBase(BaseModel):
    name: str
    address: str


class TheatreRead(TheatreBase):
    pass


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


class ActorUpdate(ActorBase):
    theatres: Optional[list[TheatreCreate]] = None


class ActorDelete(ActorRead):
    pass
