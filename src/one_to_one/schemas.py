from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Profile Schemas

class ProfileBase(BaseModel):
    title: str
    bio: str
    user_id: UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


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
    profile: Optional[ProfileBase] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    title: Optional[str] | None
    profile: Optional[ProfileUpdate] | None


class UserDelete(UserRead):
    pass
