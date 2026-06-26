from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.users import UserModel


class UserRepository:
    async def select(self, user_id: UUID, session: AsyncSession) -> UserModel | None:
        query = (
            select(UserModel)
            .where(UserModel.id ==  user_id)
            .options(selectinload(UserModel.profile))
        )

        result = await session.execute(query)
        return result.scalars().first()

    async def create(self, user: UserModel, session: AsyncSession) -> UserModel:
        session.add(user)
        return user

    async def delete(self, user: UserModel, session: AsyncSession) -> None:
        await session.delete(user)

