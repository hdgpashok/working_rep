from uuid import UUID

from sqlalchemy.orm import selectinload

from src.many_to_many.models import ActorModel, TheatreModel

from src.db import SessionDep

from src.many_to_many.schemas import ActorCreate

from sqlalchemy import select, delete


async def create_actor_in_db(actor: ActorCreate, session: SessionDep):
    new_actor = ActorModel(
        first_name=actor.first_name,
        last_name=actor.last_name,
        theatres=[TheatreModel(name=theatre.name, address=theatre.address) for theatre in actor.theatres]
    )

    session.add(new_actor)
    await session.commit()


async def get_actor_from_db(actor_id: UUID, session: SessionDep):
    query = select(ActorModel).where(ActorModel.id == actor_id).options(selectinload(ActorModel.theatres))

    result = await session.execute(query)
    return result.scalars().first()