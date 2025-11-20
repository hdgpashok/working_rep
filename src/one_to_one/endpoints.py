from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends

from src.db import get_session, SessionDep
from src.one_to_one.crud import create_user_db, get_users_db, update_user_db, delete_user_db
from src.one_to_one.schemas import UserCreate, UserRead, UserUpdate, UserDelete, UserOut

router = APIRouter(
    tags=['Пользователи и профили'],
    dependencies=[Depends(get_session)]
)


@router.post("/users", status_code=201)
async def create_user(
        user: UserCreate,
        session: SessionDep) -> UserOut:
    new_user = await create_user_db(user, session)
    return new_user


@router.get("/users/{user_id}", status_code=200)
async def get_users(
        user_id: UUID,
        session: SessionDep):
    res = await get_users_db(user_id, session)

    return res


@router.patch("/users/{user_id}",status_code=200)
async def edit_user_by_id(
        user_id: UUID,
        edited_user: UserUpdate,
        session: SessionDep) -> UserOut:

    res = await update_user_db(user_id, edited_user, session)
    return res


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
        user_id: UUID,
        session: SessionDep):
    res = await delete_user_db(user_id, session)
    return res