from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.profiles import ProfileCreate, ProfileOut, ProfileUpdate


class UserBase(BaseModel):
    title: str


class UserRead(BaseModel):
    id: UUID


class UserCreate(UserBase):
    profile: ProfileCreate


class UserOut(UserRead):
    title: str
    profile: ProfileOut

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    profile: ProfileUpdate


class UserDelete(UserRead):
    pass
