import uuid
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload

from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate, UserUpdate, UserOut
from src.exceptions.not_found import ObjectNotFound


async def get_users_db(user_id: UUID, session: AsyncSession) -> UserOut:
    query = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.profile))
    )
    result = await session.execute(query)

    user = result.scalars().first()

    if not user:
        raise ObjectNotFound(object_id=user_id)

    return UserOut.model_validate(user)


async def create_user_db(user: UserCreate, session: AsyncSession) -> UserOut:
    new_profile = ProfileModel(
        **user.profile.model_dump()
    )
    new_user = UserModel(
        id=uuid.uuid4(),
        title=user.title,

        profile=new_profile
    )

    session.add(new_user)

    return await get_users_db(new_user.id, session)


async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
    query = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.profile))
    )
    result = await session.execute(query)

    user = result.scalars().one_or_none()

    if not user:
        raise ObjectNotFound(object_id=user_id)

    user.title = updated_user.title
    user.profile = updated_user.profile

    return await get_users_db(user_id, session)


async def delete_user_db(user_id: UUID, session: AsyncSession):
    user = await session.get(UserModel, user_id)
    if not user:
        raise ObjectNotFound(object_id=user_id  )

    await session.delete(user)
    return

