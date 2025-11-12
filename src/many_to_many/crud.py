from uuid import UUID

from sqlalchemy.orm import selectinload

from fastapi import HTTPException

from src.many_to_many.models import ActorModel, TheatreModel, ActorsAndTheatres

from src.db import SessionDep

from src.many_to_many.schemas import ActorCreate, ActorUpdate

from sqlalchemy import select, delete


async def create_actor_in_db(actor: ActorCreate, session: SessionDep):
    new_actor = ActorModel(first_name=actor.first_name, last_name=actor.last_name)
    theatres = []

    for theatre in actor.theatres or []:
        result = await session.execute(
            select(TheatreModel)
            .where(TheatreModel.name == theatre.name)
            .where(TheatreModel.address == theatre.address)
        )
        existing_theatre = result.scalars().one_or_none()

        if existing_theatre:
            theatres.append(existing_theatre)
        else:
            new_theatre = TheatreModel(name=theatre.name, address=theatre.address)
            session.add(new_theatre)
            theatres.append(new_theatre)

    new_actor.theatres = theatres
    session.add(new_actor)

    await session.commit()
    await session.refresh(new_actor)


async def get_actor_from_db(actor_id: UUID, session: SessionDep):
    query = select(ActorModel).where(ActorModel.id == actor_id).options(selectinload(ActorModel.theatres))

    result = await session.execute(query)
    return result.scalars().first()


async def update_actor_in_db(actor_id: UUID, updated_actor: ActorUpdate, session: SessionDep):
    query = select(ActorModel).where(ActorModel.id == actor_id).options(selectinload(ActorModel.theatres))

    res = await session.execute(query)

    actor = res.scalars().first()

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    actor.first_name = updated_actor.first_name
    actor.last_name = updated_actor.last_name

    if updated_actor.theatres:
        actor.theatres = [TheatreModel(name=theatre.name, address=theatre.address) for theatre in updated_actor.theatres]


async def delete_actor_from_realation(actor_id: UUID, session: SessionDep):
    query = delete(ActorsAndTheatres).where(ActorsAndTheatres.actor_id == actor_id)

    await session.execute(query)


async def delete_actor_from_db(actor_id: UUID, session: SessionDep):
    await delete_actor_from_realation(actor_id, session)
    query = delete(ActorModel).where(ActorModel.id == actor_id)

    await session.execute(query)
