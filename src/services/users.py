import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.users import UserModel
from src.models.profiles import ProfileModel

from src.core.exceptions.not_found import ObjectNotFound

from src.schemas.users import UserOut, UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    async def get_users_with_profile(user_id: UUID, session: AsyncSession) -> UserOut:
        query = (
            select(UserModel)
            .where(user_id == UserModel.id)
            .options(selectinload(UserModel.profile))
        )
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise ObjectNotFound(object_id=user_id)

        return UserOut.model_validate(user)

    @staticmethod
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

        return await UserRepository.get_users_with_profile(new_user.id, session)

    @staticmethod
    async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
        query = (
            select(UserModel)
            .where(user_id == UserModel.id)
            .options(selectinload(UserModel.profile))
        )
        result = await session.execute(query)

        user = result.scalars().one_or_none()

        if not user:
            raise ObjectNotFound(object_id=user_id)

        user.title = updated_user.title
        user.profile = updated_user.profile

        return await UserRepository.get_users_with_profile(user_id, session)

    @staticmethod
    async def delete_user_db(user_id: UUID, session: AsyncSession):
        user = await session.get(UserModel, user_id)
        if not user:
            raise ObjectNotFound(object_id=user_id  )

        await session.delete(user)
        return
