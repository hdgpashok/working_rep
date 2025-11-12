from fastapi import APIRouter

from src.many_to_many.crud import create_actor_in_db

from src.db import SessionDep

from src.many_to_many.schemas import ActorCreate

router = APIRouter()


@router.post("/create_actor")
async def create_actor(actor: ActorCreate, session: SessionDep):
    await create_actor_in_db(actor, session)

    return {'status': 'actor created'}