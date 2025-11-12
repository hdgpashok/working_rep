from uuid import UUID

from fastapi import APIRouter

from src.many_to_many.crud import create_actor_in_db, get_actor_from_db

from src.db import SessionDep

from src.many_to_many.schemas import ActorCreate

router = APIRouter()


@router.post("/create_actor")
async def create_actor(actor: ActorCreate, session: SessionDep):
    await create_actor_in_db(actor, session)

    return {'status': 'actor created'}


@router.get("/get_actor/{actor_id}")
async def get_actor(actor_id: UUID, session: SessionDep):
    res = await get_actor_from_db(actor_id, session)

    return res