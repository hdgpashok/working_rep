from src.db import SessionDep
from src.one_to_one.models import UserModel, ProfileModel
from src.one_to_one.schemas import UserCreate


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
