from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate, ProfileCreate


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_user(user: UserCreate, session: SessionDep) -> None:
    new_profile = ProfileModel(
        **user.profile.model_dump()
    )
    new_user = UserModel(
        title=user.title,

        profile=new_profile
    )

    session.add(new_user)
    await session.commit()
