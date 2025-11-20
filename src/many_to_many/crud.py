from uuid import UUID

from sqlalchemy.orm import selectinload

from src.exceptions.actor import ActorNotFound

from src.many_to_many.models import ActorModel, TheatreModel, ActorsAndTheatres

from src.db import SessionDep

from src.many_to_many.schemas import ActorCreate, ActorUpdate, ActorOut

from sqlalchemy import select, delete


async def get_actor_from_db(
        actor_id: UUID,
        session: SessionDep) -> ActorOut:
    query = (
        select(ActorModel)
        .where(ActorModel.id == actor_id)
        .options(selectinload(ActorModel.theatres))
    )
    result = await session.execute(query)
    actor = result.scalars().first()

    if not actor:
        raise ActorNotFound(actor_id=actor_id)

    return ActorOut.model_validate(actor)


async def create_actor_in_db(
        actor: ActorCreate,
        session: SessionDep) -> ActorOut:
    new_actor = ActorModel(**actor.model_dump(exclude={'theatres'}))

    for theatre_data in actor.theatres or []:
        query = (
            select(TheatreModel)
            .where(TheatreModel.name == theatre_data.name)
            .where(TheatreModel.address == theatre_data.address)
        )
        result = await session.execute(query)
        theatre = result.scalars().one_or_none()

        if theatre is None:
            theatre = TheatreModel(**theatre_data.model_dump())

        new_actor.theatres.append(theatre)

    session.add(new_actor)
    await session.commit()
    await session.refresh(new_actor)

    res = await get_actor_from_db(new_actor.id, session)
    return res


async def update_actor_in_db(
        actor_id: UUID,
        updated_actor: ActorUpdate,
        session: SessionDep) -> ActorOut:
    query = (
        select(ActorModel)
        .where(ActorModel.id == actor_id)
        .options(selectinload(ActorModel.theatres))
    )

    res = await session.execute(query)

    actor = res.scalars().first()
    actor.first_name = updated_actor.first_name
    actor.last_name = updated_actor.last_name

    if updated_actor.theatres:
        actor.theatres = [TheatreModel(name=theatre.name, address=theatre.address) for theatre in updated_actor.theatres]

    await session.commit()
    res = await get_actor_from_db(actor_id, session)
    return res


async def delete_actor_from_realation(actor_id: UUID, session: SessionDep):
    query = delete(ActorsAndTheatres).where(ActorsAndTheatres.actor_id == actor_id)

    await session.execute(query)


async def delete_actor_from_db(
        actor_id: UUID,
        session: SessionDep):
    await get_actor_from_db(actor_id, session)
    await delete_actor_from_realation(actor_id, session)
    query = delete(ActorModel).where(ActorModel.id == actor_id)
    await session.execute(query)

    return