from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends

from src.many_to_many.crud import create_actor_in_db, get_actor_from_db, update_actor_in_db, delete_actor_from_db

from src.db import SessionDep, get_session

from src.many_to_many.schemas import ActorCreate, ActorUpdate, ActorOut

router = APIRouter(
    tags=['Актеры и театры'],
    dependencies=[Depends(get_session)]
)


@router.post("/actors")
async def create_actor(actor: ActorCreate, session: SessionDep) -> Dict[str, str]:
    await create_actor_in_db(actor, session)

    return {'status': 'actor created'}


@router.get("/actors/{actor_id}")
async def get_actor(actor_id: UUID, session: SessionDep) -> ActorOut:
    res = await get_actor_from_db(actor_id, session)

    return res


@router.patch("/actors/{actor_id}")
async def edit_actor(actor_id: UUID, updated_actor: ActorUpdate, session: SessionDep) -> Dict[str, str]:
    await update_actor_in_db(actor_id, updated_actor, session)
    return {"status": 'actor edited'}


@router.delete("/actors/{actor_id}")
async def delete_actor(actor_id: UUID, session: SessionDep) -> Dict[str, str]:
    await delete_actor_from_db(actor_id, session)

    return {'status': 'actor deleted'}