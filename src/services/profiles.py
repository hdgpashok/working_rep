import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profiles import ProfileModel

from src.exceptions.not_found import ObjectNotFound

from src.schemas.profiles import ProfileOut, ProfileCreate, ProfileUpdate


class ProfileService:
    @staticmethod
    async def get_profile(profile_id: UUID, session: AsyncSession) -> ProfileOut:
        query = (
            select(ProfileModel)
            .where(profile_id == ProfileModel.id)
        )
        result = await session.execute(query)
        profile = result.scalars().first()

        if not profile:
            raise ObjectNotFound(object_id=profile_id)

        return ProfileOut.model_validate(profile)

    @staticmethod
    async def create_profile(user: ProfileCreate, session: AsyncSession) -> ProfileOut:
        new_profile = ProfileModel(
            id=uuid.uuid4(),
            **user.profile.model_dump()
        )
        session.add(new_profile)

        return await ProfileService.get_profile(new_profile.id, session)

    @staticmethod
    async def update_profile(profile_id: UUID, profile: ProfileUpdate, session: AsyncSession) -> UserOut:
        query = (
            select(ProfileModel)
            .where(profile_id == ProfileModel.id)
        )
        result = await session.execute(query)

        updated_profile = result.scalars().one_or_none()

        if not profile:
            raise ObjectNotFound(object_id=profile_id)

        for key, value in profile.model_dump(exclude_unset=True).items():
            setattr(updated_profile, key, value)

        return await ProfileService.get_profile(profile_id, session)

    @staticmethod
    async def delete_profile(profile_id: UUID, session: AsyncSession):
        profile = await session.get(ProfileModel, profile_id)
        if not profile:
            raise ObjectNotFound(object_id=profile_id)

        await session.delete(profile)
        return
