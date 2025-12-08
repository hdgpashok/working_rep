import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.theatres import TheatreModel
from src.models.actors import ActorModel

from src.core.exceptions.not_found import ObjectNotFound
from src.schemas.actors import ActorOut, ActorCreate, ActorUpdate


class ActorRepository:
    @staticmethod
    async def get_actor_from_db(actor_id: UUID, session: AsyncSession) -> ActorOut:
        query = (
            select(ActorModel)
            .where(actor_id == ActorModel.id)
            .options(selectinload(ActorModel.theatres))
        )
        result = await session.execute(query)
        actor = result.scalars().first()

        if not actor:
            raise ObjectNotFound(object_id=actor_id)

        return ActorOut.model_validate(actor)

    @staticmethod
    async def create_actor_in_db(actor: ActorCreate, session: AsyncSession) -> ActorOut:
        new_actor = ActorModel(
            id=uuid.uuid4(),
            **actor.model_dump(exclude={'theatres'})
        )

        new_actor.theatres = []
        for theatre in actor.theatres:
            query = (
                select(TheatreModel).filter(
                    theatre.name == TheatreModel.name,
                    )
            )
            result = await session.execute(query)
            db_theatre = result.scalars().one_or_none()

            if not db_theatre:
                db_theatre = TheatreModel(**theatre.model_dump())

            new_actor.theatres.append(db_theatre)

        session.add(new_actor)

        return await ActorRepository.get_actor_from_db(new_actor.id, session)

    @staticmethod
    async def update_actor_in_db(actor_id: UUID, updated_actor: ActorUpdate, session: AsyncSession) -> ActorOut:
        query = (
            select(ActorModel)
            .filter(actor_id == ActorModel.id)
            .options(selectinload(ActorModel.theatres))
        )

        res = await session.execute(query)

        actor = res.scalars().one_or_none()

        if not actor:
            raise ObjectNotFound(object_id=actor_id)

        for f_name, l_name in updated_actor.model_dump(exclude={'theatres'}, exclude_unset=True).items():
            setattr(actor, f_name, l_name)

        actor.theatres = []

        for theatre in updated_actor.theatres:
            query = (
                select(TheatreModel).filter(
                    theatre.name == TheatreModel.name,
                    theatre.address == TheatreModel.address
                )
            )
            result = await session.execute(query)
            db_theatre = result.scalars().one_or_none()

            if not db_theatre:
                db_theatre = TheatreModel(**theatre.model_dump())

            actor.theatres.append(db_theatre)

        return await ActorRepository.get_actor_from_db(actor_id, session)

    @staticmethod
    async def delete_actor_from_db(actor_id: UUID, session: AsyncSession):
        actor = await session.get(ActorModel, actor_id)
        if not actor:
            raise ObjectNotFound(object_id=actor_id)

        await session.delete(actor)
        return