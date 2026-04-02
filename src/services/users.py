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

        logger.info(f'[GET USER] Start user_id={user_id}')

        cache = await rd.get(key)
        if cache:
            logger.info(f'[GET USER] Cache hit user_id={user_id}')
            user = json.loads(cache)
            return UserOut.model_validate(user)

        try:
            user = await UserRepository.select(user_id, session)
            logger.info(f'[GET USER] Fetched from DB user_id={user_id}')
        except Exception as exc:
            logger.error(
                f'[GET USER] DB error user_id={user_id} error={repr(exc)}'
            )
            raise

        try:
            await rd.set(
                key,
                UserOut.model_validate(user).model_dump_json(),
                ex=expire_time
            )
            logger.info(f'[GET USER] Cached user user_id={user_id}')
        except Exception as exc:
            logger.warning(
                f'[GET USER] Cache write failed user_id={user_id} error={repr(exc)}'
            )

        logger.info(f'[GET USER] Success user_id={user_id}')
        return UserOut.model_validate(user)

    @staticmethod
    async def create_user_db(user: UserCreate, session: AsyncSession) -> UserOut:
        logger.info(f'[CREATE USER] Start')

        try:
            result = await UserRepository.create_user_db(user, session)
            logger.info(f'[CREATE USER] Success')
            return result
        except Exception as exc:
            logger.error(
                f'[CREATE USER] DB error error={repr(exc)}'
            )
            raise

    @staticmethod
    async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
        logger.info(f'[UPDATE USER] Start user_id={user_id}')

        try:
            result = await UserRepository.update_user_db(user_id, updated_user, session)
            logger.info(f'[UPDATE USER] Success user_id={user_id}')
            return result
        except Exception as exc:
            logger.error(
                f'[UPDATE USER] DB error user_id={user_id} error={repr(exc)}'
            )
            raise

    @staticmethod
    async def delete_user_db(user_id: UUID, session: AsyncSession):
        logger.info(f'[DELETE USER] Start user_id={user_id}')

        try:
            result = await UserRepository.delete_user_db(user_id, session)
            logger.info(f'[DELETE USER] Success user_id={user_id}')
            return result
        except Exception as exc:
            logger.error(
                f'[DELETE USER] DB error user_id={user_id} error={repr(exc)}'
            )
            raise

    @staticmethod
    async def create_external_user(user: UserExternal, session: AsyncSession) -> UserOut:
        logger.info(f'[CREATE EXTERNAL USER] Start user_id={user.id}')

        try:
            result = await UserRepository.create_external_user(user, session)
            logger.info(f'[CREATE EXTERNAL USER] Success user_id={user.id}')
            return result
        except Exception as exc:
            logger.error(
                f'[CREATE EXTERNAL USER] DB error user_id={user.id} error={repr(exc)}'
            )
            raise