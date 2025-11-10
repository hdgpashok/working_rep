from typing import Dict
from uuid import UUID

from fastapi import APIRouter

from src.db import SessionDep
from src.one_to_one.crud import create_user_db, get_users_db
from src.one_to_one.schemas import UserCreate, UserRead

router = APIRouter()


@router.post("/create_user")
async def create_user(
        user: UserCreate,
        session: SessionDep) -> Dict[str, str]:

    await create_user_db(user, session)
    return {'status': 'user created'}


@router.get("/get_users/{user_id}")
async def get_users(user_id: UUID, session: SessionDep):
    res = await get_users_db(user_id, session)

    return res