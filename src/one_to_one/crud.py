from uuid import UUID

from sqlalchemy import select, delete

from sqlalchemy.orm import selectinload

from src.db import SessionDep
from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate, UserUpdate, UserOut
from src.exceptions.user import UserNotFound


async def get_users_db(
        user_id: UUID,
        session: SessionDep) -> UserOut:
    query = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.profile))
    )
    result = await session.execute(query)

    user = result.scalars().first()

    if not user:
        raise UserNotFound(user_id=user_id)

    return UserOut.model_validate(user)


async def create_user_db(
        user: UserCreate,
        session: SessionDep) -> UserOut:
    new_profile = ProfileModel(
        **user.profile.model_dump()
    )
    new_user = UserModel(
        title=user.title,

        profile=new_profile
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    res = await get_users_db(new_user.id, session)
    return res


async def update_user_db(
        user_id: UUID,
        updated_user: UserUpdate,
        session: SessionDep) -> UserOut:
    query = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.profile))
    )
    result = await session.execute(query)

    user = result.scalars().first()

    user.title = updated_user.title
    user.profile.title = updated_user.profile.title
    user.profile.bio = updated_user.profile.bio

    await session.commit()
    res = await get_users_db(user_id, session)
    return res


async def delete_profile_db(
        user_id: UUID,
        session: SessionDep):
    query = delete(ProfileModel).where(ProfileModel.user_id == user_id)
    await session.execute(query)


async def delete_user_db(
        user_id: UUID,
        session: SessionDep):
    res = await get_users_db(user_id, session)
    await delete_profile_db(user_id, session)
    query = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(query)

    return

