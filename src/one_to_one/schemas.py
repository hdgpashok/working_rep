import uuid
from typing import Optional

from pydantic import BaseModel


# Profile Schemas

class ProfileBase(BaseModel):
    title: str
    bio: str


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: uuid

    class Config:
        orm_mode = True


# User Schemas

class UserBase(BaseModel):
    title: str


class UserCreate(UserBase):
    profile: ProfileCreate


class UserRead(UserBase):
    id: uuid
    profile: Optional[ProfileRead] = None

    class Config:
        orm_mode = True
