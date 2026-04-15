from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.users import UserModel

from src.exceptions.not_found import ObjectNotFound

from src.schemas.users import UserOut, UserCreate, UserUpdate, UserExternal

from src.core.logger import get_logger

from src.mapping import DataMapping


user_repo_logger = get_logger('user_repo')


class UserRepository:
    @staticmethod
    async def select(user_id: UUID, session: AsyncSession):
        query = (
            select(UserModel)
            .where(user_id == UserModel.id)
            .options(selectinload(UserModel.profile))
        )
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise ObjectNotFound(object_id=user_id)

        return user

    @staticmethod
    async def create_user_db(user: UserCreate, session: AsyncSession) -> UserOut:
        new_user = DataMapping.map_create_data(user)
        session.add(new_user)

        db_user = await UserRepository.select(new_user.id, session)
        return UserOut.model_validate(db_user)

    @staticmethod
    async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
        user = await UserRepository.select(user_id, session)

        DataMapping.map_update_user(user, updated_user)

        user = await UserRepository.select(user_id, session)
        return UserOut.model_validate(user)

    @staticmethod
    async def delete_user_db(user_id: UUID, session: AsyncSession):
        user = await session.get(UserModel, user_id)
        if not user:
            raise ObjectNotFound(object_id=user_id)

        await session.delete(user)
        return

    @staticmethod
    async def create_external_user(user: UserExternal, session: AsyncSession) -> UserOut:
        new_user = DataMapping.map_external_user(user)

        session.add(new_user)

        return UserOut.model_validate(new_user)