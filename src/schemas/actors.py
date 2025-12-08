from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.theatres import TheatreCreate, TheatreOut, TheatreUpdate


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorRead(BaseModel):
    id: UUID


class ActorCreate(ActorBase):
    theatres: list[TheatreCreate]


class ActorOut(ActorBase):
    id: UUID
    theatres: list[TheatreOut]

    model_config = ConfigDict(from_attributes=True)


class ActorUpdate(ActorBase):
    theatres: list[TheatreUpdate]


class ActorDelete(ActorRead):
    pass
