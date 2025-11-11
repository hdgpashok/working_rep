from fastapi import APIRouter

from src.db import SessionDep

from src.one_to_many.schemas import AuthorCreate

from src.one_to_many.crud import create_author_in_db


router = APIRouter()


@router.post("/create_author")
async def create_author(author: AuthorCreate, session: SessionDep):
    await create_author_in_db(author, session)
    return {'status': 'user created'}
