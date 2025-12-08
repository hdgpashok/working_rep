from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.db import get_session, SessionDep
from src.one_to_one.crud import create_user_db, get_users_db, update_user_db, delete_user_db
from src.one_to_one.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(
    prefix="/api/v1/users_profiles",
    tags=['Пользователи и профили'],
    dependencies=[Depends(get_session)]
)


@router.post("/users", status_code=HTTP_201_CREATED)
async def create_user(user: UserCreate, session: SessionDep) -> UserOut:
    return await create_user_db(user, session)


@router.get("/users/{user_id}", status_code=HTTP_200_OK)
async def get_users(user_id: UUID, session: SessionDep):
    return await get_users_db(user_id, session)


@router.patch("/users/{user_id}",status_code=HTTP_200_OK)
async def edit_user_by_id(user_id: UUID, edited_user: UserUpdate, session: SessionDep) -> UserOut:
    return await update_user_db(user_id, edited_user, session)


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, session: SessionDep):
    return await delete_user_db(user_id, session)
