from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends

from src.db import SessionDep, get_session

from src.one_to_many.schemas import AuthorCreate, AuthorOut, AuthorUpdate

from src.one_to_many.crud import create_author_in_db, get_author_from_db, edit_author_in_db, delete_author_from_db

router = APIRouter(
    tags=['Авторы и книги'],
    dependencies=[Depends(get_session)]
)


@router.post("/authors", status_code=201)
async def create_author(
        author: AuthorCreate,
        session: SessionDep) -> AuthorOut:
    author = await create_author_in_db(author, session)
    return author


@router.get("/authors/{author_id}", status_code=200)
async def get_author(
        author_id: UUID,
        session: SessionDep) -> AuthorOut:
    result = await get_author_from_db(author_id, session)
    return result


@router.patch("/authors/{author_id}", status_code=200)
async def edit_author(
        author_id: UUID,
        author: AuthorUpdate,
        session: SessionDep) -> AuthorOut:
    author = await edit_author_in_db(author_id, author, session)
    return author


@router.delete("/authors/{author_id}", status_code=204)
async def delete_author(
        author_id: UUID,
        session: SessionDep):
    res = await delete_author_from_db(author_id, session)
    return res