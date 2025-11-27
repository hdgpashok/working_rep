from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.many_to_many.crud import create_actor_in_db, get_actor_from_db, update_actor_in_db, delete_actor_from_db

from src.db import SessionDep, get_session

from src.many_to_many.schemas import ActorCreate, ActorUpdate, ActorOut


router = APIRouter(
    tags=['Актеры и театры'],
    dependencies=[Depends(get_session)]
)


@router.post("/actors", status_code=HTTP_201_CREATED)
async def create_actor(
        actor: ActorCreate,
        session: SessionDep) -> ActorOut:
    res = await create_actor_in_db(actor, session)
    return res


@router.get("/actors/{actor_id}", status_code=HTTP_200_OK)
async def get_actor(
        actor_id: UUID,
        session: SessionDep) -> ActorOut:
    res = await get_actor_from_db(actor_id, session)
    return res


@router.patch("/actors/{actor_id}", status_code=HTTP_200_OK)
async def edit_actor(
        actor_id: UUID,
        updated_actor: ActorUpdate,
        session: SessionDep) -> ActorOut:
    res = await update_actor_in_db(actor_id, updated_actor, session)
    return res


@router.delete("/actors/{actor_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_actor(actor_id: UUID, session: SessionDep):
    res = await delete_actor_from_db(actor_id, session)
    return res