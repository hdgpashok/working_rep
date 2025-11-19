from uuid import UUID

from sqlalchemy import select, delete

from sqlalchemy.orm import selectinload

from src.db import SessionDep
from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate, UserUpdate
from src.exceptions.user import UserNotFound


async def create_user_db(user: UserCreate, session: SessionDep) -> None:
    new_profile = ProfileModel(
        **user.profile.model_dump()
    )
    new_user = UserModel(
        title=user.title,

        profile=new_profile
    )

    session.add(new_user)
    await session.commit()


async def get_users_db(user_id: UUID, session: SessionDep):
    query = select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.profile))
    result = await session.execute(query)

    user = result.scalars().first()

    if not user:
        raise UserNotFound(user_id=user_id)

    return user


async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: SessionDep):
    user = await get_users_db(user_id, session)

    if updated_user.title is not None:
        user.title = updated_user.title

    if updated_user.profile is not None:
        if user.profile:
            if updated_user.profile.title is not None:
                user.profile.title = updated_user.profile.title
            if updated_user.profile.bio is not None:
                user.profile.bio = updated_user.profile.bio

    session.add(user)
    await session.commit()


async def delete_profile_db(user_id: UUID, session: SessionDep):
    query = delete(ProfileModel).where(ProfileModel.user_id == user_id)
    await session.execute(query)


async def delete_user_db(user_id: UUID, session: SessionDep):
    await delete_profile_db(user_id, session)
    query = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(query)

