import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.theatres import TheatreModel

from src.exceptions.not_found import ObjectNotFound

from src.schemas.theatres import TheatreOut, TheatreCreate, TheatreUpdate


class TheatreService:
    @staticmethod
    async def get_theatre(theatre_id: UUID, session: AsyncSession) -> TheatreOut:
        query = (
            select(TheatreModel)
            .where(theatre_id == TheatreModel.id)
        )
        result = await session.execute(query)
        theatre = result.scalars().first()

        if not theatre:
            raise ObjectNotFound(object_id=theatre_id)

        return TheatreOut.model_validate(theatre)

    @staticmethod
    async def create_profile(theatre: TheatreCreate, session: AsyncSession) -> TheatreOut:
        new_theatre = TheatreModel(
            id=uuid.uuid4(),
            **theatre.profile.model_dump()
        )
        session.add(new_theatre)

        return await TheatreService.get_theatre(new_theatre.id, session)

    @staticmethod
    async def update_profile(theatre_id: UUID, theatre: TheatreUpdate, session: AsyncSession) -> TheatreOut:
        query = (
            select(TheatreModel)
            .where(theatre_id == TheatreModel.id)
        )
        result = await session.execute(query)

        updated_theatre = result.scalars().one_or_none()

        if not updated_theatre:
            raise ObjectNotFound(object_id=theatre_id)

        for key, value in theatre.model_dump(exclude_unset=True).items():
            setattr(updated_theatre, key, value)

        return await TheatreService.get_theatre(theatre_id, session)

    @staticmethod
    async def delete_theatre(theatre_id: UUID, session: AsyncSession):
        theatre = await session.get(TheatreModel, theatre_id)
        if not theatre:
            raise ObjectNotFound(object_id=theatre_id)

        await session.delete(theatre)
        return
