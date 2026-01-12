from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserOut, UserCreate, UserUpdate, UserExternal

from src.repository.user import UserRepository


class UserService:
    @staticmethod
    async def get_users_with_profile(user_id: UUID, session: AsyncSession) -> UserOut:
        return await UserRepository.get_users_with_profile(user_id, session)

    @staticmethod
    async def create_user_db(user: UserCreate, session: AsyncSession) -> UserOut:
        return await UserRepository.create_user_db(user, session)

    @staticmethod
    async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
        return await UserRepository.update_user_db(user_id, updated_user, session)

    @staticmethod
    async def delete_user_db(user_id: UUID, session: AsyncSession):
        return await UserRepository.delete_user_db(user_id, session)

    @staticmethod
    async def create_external_user(user: UserExternal, session: AsyncSession) -> UserOut:
        return await UserRepository.create_external_user(user, session)
