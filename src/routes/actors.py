from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.services.actors import ActorRepository
from src.db import SessionDep, get_session

from src.schemas.actors import ActorCreate, ActorUpdate, ActorOut


router = APIRouter(
    prefix='/api/v1/actors_theatres',
    tags=['Актеры и театры'],
    dependencies=[Depends(get_session)]
)


@router.post("/actors", status_code=HTTP_201_CREATED)
async def create_actor(actor: ActorCreate, session: SessionDep) -> ActorOut:
    return await ActorRepository.create_actor_in_db(actor, session)


@router.get("/actors/{actor_id}", status_code=HTTP_200_OK)
async def get_actor(actor_id: UUID, session: SessionDep) -> ActorOut:
    return await ActorRepository.get_actor_from_db(actor_id, session)


@router.patch("/actors/{actor_id}", status_code=HTTP_200_OK)
async def edit_actor(actor_id: UUID, updated_actor: ActorUpdate, session: SessionDep) -> ActorOut:
    return await ActorRepository.update_actor_in_db(actor_id, updated_actor, session)


@router.delete("/actors/{actor_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_actor(actor_id: UUID, session: SessionDep):
    return await ActorRepository.delete_actor_from_db(actor_id, session)
