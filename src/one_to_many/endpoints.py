from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends

from src.db import SessionDep, get_session

from src.one_to_many.schemas import AuthorCreate, AuthorEdit, AuthorOut

from src.one_to_many.crud import create_author_in_db, get_author_from_db, edit_author_in_db, delete_author_from_db

router = APIRouter(
    tags=['Авторы и книги'],
    dependencies=Depends[get_session]
)


@router.post("/create_author")
async def create_author(author: AuthorCreate, session: SessionDep) -> Dict[str, str]:
    await create_author_in_db(author, session)
    return {'status': 'user created'}


@router.get("/get_author/{author_id}")
async def get_author(author_id: UUID, session: SessionDep) -> AuthorOut:
    result = await get_author_from_db(author_id, session)

    return result


@router.patch("/edit_author/{author_id}")
async def edit_author(author_id: UUID, author: AuthorEdit, session: SessionDep) -> Dict[str, str]:
    await edit_author_in_db(author_id, author, session)

    return {'status': 'author edited'}


@router.delete("/delete_author/{author_id}")
async def delete_author(author_id: UUID, session: SessionDep) -> Dict[str, str]:
    await delete_author_from_db(author_id, session)

    return {'status': 'author deleted'}