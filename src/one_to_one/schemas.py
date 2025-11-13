from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Profile Schemas

class ProfileBase(BaseModel):
    title: str
    bio: str
    user_id: UUID


class ProfileCreate(BaseModel):
    title: str
    bio: str


class ProfileRead(ProfileBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProfileOut(ProfileCreate):
    id: UUID


class ProfileUpdate(BaseModel):
    title: Optional[str]
    bio: Optional[str]


class ProfileDelete(ProfileRead):
    pass


# User Schemas

class UserBase(BaseModel):
    title: str


class UserCreate(UserBase):
    profile: ProfileCreate


class UserRead(UserBase):
    id: UUID


class UserOut(UserBase):
    profile: Optional[ProfileOut]
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    title: Optional[str] | None
    profile: Optional[ProfileUpdate] | None


class UserDelete(UserRead):
    pass
