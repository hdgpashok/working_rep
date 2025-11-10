import uuid
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Profile Schemas

class ProfileBase(BaseModel):
    title: str
    bio: str


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


# User Schemas

class UserBase(BaseModel):
    title: str


class UserCreate(UserBase):
    profile: ProfileCreate


class UserRead(UserBase):
    id: UUID
    profile: Optional[ProfileRead] = None

    model_config = ConfigDict(from_attributes=True)
