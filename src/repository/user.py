import json
import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.users import UserModel
from src.models.profiles import ProfileModel

from src.exceptions.not_found import ObjectNotFound

from src.schemas.users import UserOut, UserCreate, UserUpdate

from src.core.redis_cache import rd, expire_time

from src.core.logger import get_logger


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
    async def get_users_with_profile(user_id: UUID, session: AsyncSession) -> UserOut:
        key = f'user:{user_id}'
        cache = await rd.get(key)

        if cache:
            user_repo_logger.info(f'user {user_id} found in cache')
            user = json.loads(cache)
            return UserOut.model_validate(user)

        user_repo_logger.info(f'cant find in cache')

        user = await UserRepository.select(user_id, session)

        await rd.set(key, UserOut.model_validate(user).model_dump_json(), ex=expire_time)
        user_repo_logger.info(f'user:{user_id} cached')
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

        db_user = await UserRepository.select(new_user.id, session)
        return UserOut.model_validate(db_user)

    @staticmethod
    async def update_user_db(user_id: UUID, updated_user: UserUpdate, session: AsyncSession) -> UserOut:
        user = await UserRepository.select(user_id, session)

        data = updated_user.model_dump(exclude={'profile'})
        for key, value in data.items():
            setattr(user, key, value)

        profile_data = updated_user.profile.model_dump()
        for key, value in profile_data.items():
            setattr(user.profile, key, value)

        user = await UserRepository.select(user_id, session)
        return UserOut.model_validate(user)

    @staticmethod
    async def delete_user_db(user_id: UUID, session: AsyncSession):
        user = await session.get(UserModel, user_id)
        if not user:
            raise ObjectNotFound(object_id=user_id)

        await session.delete(user)
        return {'info': 'user deleted'}
