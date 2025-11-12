from typing import Optional

from pydantic import BaseModel


class TheatreBase(BaseModel):
    name: str
    address: str


class TheatreRead(TheatreBase):
    pass


class TheatreCreate(TheatreBase):
    pass


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    theatres: Optional[list[TheatreCreate]] = None


class ActorRead(ActorBase):
    pass
