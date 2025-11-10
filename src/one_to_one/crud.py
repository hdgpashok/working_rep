from uuid import UUID

from sqlalchemy.orm import selectinload

from src.db import SessionDep
from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate, UserRead

from sqlalchemy import select


async def create_user_db(user: UserCreate, session: SessionDep) -> None:
    new_profile = ProfileModel(
        **user.profile.model_dump()
    )
    new_user = UserModel(
        title=user.title,

        profile=new_profile
    )

    session.add(new_user)
    await session.commit()


async def get_users_db(user_id: UUID, session: SessionDep):
    query = select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.profile))
    result = await session.execute(query)

    return result.scalars().all()
