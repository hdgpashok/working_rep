from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TheatreBase(BaseModel):
    name: str
    address: str


class TheatreRead(BaseModel):
    id: UUID


class TheatreOut(TheatreBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TheatreCreate(TheatreBase):
    pass


class TheatreUpdate(TheatreBase):
    pass


class TheatreDelete(TheatreRead):
    pass