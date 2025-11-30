from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.exceptions.not_found import ObjectNotFound

from src.many_to_many.models import ActorModel, TheatreModel

from src.many_to_many.schemas import ActorCreate, ActorUpdate, ActorOut

from sqlalchemy import select


async def get_actor_from_db(
        actor_id: UUID,
        session: AsyncSession) -> ActorOut:
    query = (
        select(ActorModel)
        .where(ActorModel.id == actor_id)
        .options(selectinload(ActorModel.theatres))
    )
    result = await session.execute(query)
    actor = result.scalars().first()

    if not actor:
        raise ObjectNotFound(object_id=actor_id)

    return ActorOut.model_validate(actor)


async def create_actor_in_db(
        actor: ActorCreate,
        session: AsyncSession) -> ActorOut:
    new_actor = ActorModel(**actor.model_dump(exclude={'theatres'}))

    new_actor.theatres = []
    for theatre in actor.theatres:
        query = (
            select(TheatreModel).filter(
                TheatreModel.name == theatre.name,
                TheatreModel.address == theatre.address
            )
        )
        result = await session.execute(query)
        db_theatre = result.scalars().one_or_none()

        if not db_theatre:
            db_theatre = TheatreModel(**theatre.model_dump())

        new_actor.theatres.append(db_theatre)

    session.add(new_actor)

    await session.flush()

    res = await get_actor_from_db(new_actor.id, session)
    return res


async def update_actor_in_db(
        actor_id: UUID,
        updated_actor: ActorUpdate,
        session: AsyncSession) -> ActorOut:
    query = (
        select(ActorModel)
        .filter(ActorModel.id == actor_id)
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
                TheatreModel.name == theatre.name,
                TheatreModel.address == theatre.address
            )
        )
        result = await session.execute(query)
        db_theatre = result.scalars().one_or_none()

        if not db_theatre:
            db_theatre = TheatreModel(**theatre.model_dump())

        actor.theatres.append(db_theatre)

    res = await get_actor_from_db(actor_id, session)
    return res


async def delete_actor_from_db(
        actor_id: UUID,
        session: AsyncSession):
    actor = await session.get(ActorModel, actor_id)
    if not actor:
        raise ObjectNotFound(object_id=actor_id)

    await session.delete(actor)
    return