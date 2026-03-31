import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserOut, UserCreate, UserUpdate, UserExternal

from src.core.redis_cache import rd, expire_time

from src.core.logger import get_logger

from src.repository.user import UserRepository

logger = get_logger('service_logger')


class UserService:
    @staticmethod
    async def get_users_with_profile(user_id: UUID, session: AsyncSession) -> UserOut:
        key = f'user:{user_id}'
        cache = await rd.get(key)

        if cache:
            logger.info('cache hit')
            user = json.loads(cache)
            return UserOut.model_validate(user)

        user = await UserRepository.select(user_id, session)

        await rd.set(key, UserOut.model_validate(user).model_dump_json(), ex=expire_time)
        logger.info(f'new key in cache\n {key}')
        return UserOut.model_validate(user)

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
