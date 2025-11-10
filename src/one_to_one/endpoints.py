from typing import Dict

from fastapi import APIRouter

from src.db import SessionDep
from src.one_to_one.crud import create_user_db
from src.one_to_one.schemas import UserCreate


router = APIRouter()


@router.post("/create_user")
async def create_user(
        user: UserCreate,
        session: SessionDep) -> Dict[str, str]:

    await create_user_db(user, session)
    return {'status': 'user created'}
