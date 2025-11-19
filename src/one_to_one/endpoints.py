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


@router.post("/create_user")
async def create_user(
        user: UserCreate,
        session: SessionDep) -> Dict[str, str]:
    await create_user_db(user, session)
    return {'status': 'user created'}


@router.get("/get_users/{user_id}")
async def get_users(
        user_id: UUID,
        session: SessionDep) -> UserOut:
    res = await get_users_db(user_id, session)

    return res


@router.patch("/edit_user_by_id/{user_id}")
async def edit_user_by_id(
        user_id: UUID,
        edited_user: UserUpdate,
        session: SessionDep) -> Dict[str, str]:
    try:
        await update_user_db(user_id, edited_user, session)
        return {'status': 'user edited'}
    except Exception as e:
        return {'error': f"{e}"}


@router.delete("/delete_user")
async def delete_user(user: UUID, session: SessionDep) -> Dict[str, str]:
    await delete_user_db(user, session)
    return {"status": "user deleted"}