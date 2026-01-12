from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    title: str
    bio: str


class ProfileRead(BaseModel):
    id: UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(ProfileBase):
    pass


class ProfileDelete(ProfileRead):
    pass


class ProfileExternal(ProfileCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)