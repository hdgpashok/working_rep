import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.repository import RepositoryDep
from src.exceptions.not_found import ObjectNotFound
from src.exceptions.server_error import ServerError

from src.schemas.users import (
    UserOut,
    UserCreate,
    UserUpdate,
    UserExternal
)

from src.utils.logger import get_logger
from redis_cache import CacheService
from src.mapping import DataMapping


logger = get_logger('service_logger')


class UserService:

    def __init__(self, cache: CacheService, repo: RepositoryDep):
        self.cache = cache
        self.repo = repo

    async def create_user_db(self, user: UserCreate, session: AsyncSession) -> UserOut:

        logger.info('[CREATE USER] Start')

        try:
            db_user = DataMapping.map_create_data(user)

            await self.repo.create(db_user, session)

            db_user = await self.repo.select(db_user.id, session)

            result = UserOut.model_validate(db_user)

            logger.info('[CREATE USER] Success')

            return result

        except Exception as exc:
            logger.error(f'[CREATE USER] DB error error={repr(exc)}')
            raise ServerError('Failed to create user in database') from exc

    async def update_user_db(self, user_id: uuid.UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:

        logger.info(f'[UPDATE USER] Start user_id={user_id}')

        user = await self.repo.select(user_id, session)

        if not user:
            raise ObjectNotFound(object_id=str(user_id))

        DataMapping.map_update_user(user, updated_user)

        result = UserOut.model_validate(user)

        await self.cache.set(f'user:{user_id}', result.model_dump(mode='json'), expire=3600)

        logger.info(f'[UPDATE USER] Success update and cached user_id={user_id}')

        return result

    async def delete_user_db(self, user_id: uuid.UUID, session: AsyncSession):

        logger.info(f'[DELETE USER] Start user_id={user_id}')

        user = await self.repo.select(user_id, session)

        if not user:
            raise ObjectNotFound(object_id=str(user_id))

        await self.repo.delete(user, session)

        logger.info(f'[DELETE USER] Success user_id={user_id}')

    async def create_external_user(self, user: UserExternal, session: AsyncSession) -> UserOut:

        logger.info(f'[CREATE EXTERNAL USER] Start user_id={user.id}')

        db_user = DataMapping.map_external_user(user)

        await self.repo.create(db_user, session)

        result = UserOut.model_validate(db_user)

        logger.info(f'[CREATE EXTERNAL USER] Success user_id={user.id}')

        return result

    async def get_users_with_profile(self, user_id: uuid.UUID, session: AsyncSession) -> UserOut:

        key = f'user:{user_id}'

        logger.info(f'[GET USER] Start user_id={user_id}')

        cached = await self.cache.get(key)

        if cached:
            logger.info(f'[GET USER] Cache hit user_id={user_id}')
            return UserOut.model_validate(cached)

        user = await self.repo.select(user_id, session)

        if not user:
            logger.warning(f'[GET USER] User not found user_id={user_id}')
            raise ObjectNotFound(object_id=str(user_id))

        result = UserOut.model_validate(user)

        await self.cache.set(key, result.model_dump(mode='json'), expire=3600)

        logger.info(f'[GET USER] Success user_id={user_id}')

        return result