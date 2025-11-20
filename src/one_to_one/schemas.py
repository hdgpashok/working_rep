from uuid import UUID

from pydantic import BaseModel, ConfigDict


# Profile Schemas

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


# User Schemas

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
