from uuid import UUID

from fastapi import APIRouter, Depends

from src.db import SessionDep, get_session

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.schemas.authors import AuthorCreate, AuthorOut, AuthorUpdate

from src.services.authors import AuthorRepository


router = APIRouter(
    prefix="/api/v1/authors_books",
    tags=['Авторы и книги'],
    dependencies=[Depends(get_session)]
)


@router.post("/authors", status_code=HTTP_201_CREATED)
async def create_author(author: AuthorCreate, session: SessionDep) -> AuthorOut:
    return await AuthorRepository.create_author_in_db(author, session)


@router.get("/authors/{author_id}")
async def get_author(author_id: UUID, session: SessionDep) -> AuthorOut:
    return await AuthorRepository.get_author_from_db(author_id, session)


@router.patch("/authors/{author_id}")
async def edit_author(author_id: UUID, author: AuthorUpdate, session: SessionDep) -> AuthorOut:
    return await AuthorRepository.edit_author_in_db(author_id, author, session)


@router.delete("/authors/{author_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID, session: SessionDep):
    return await AuthorRepository.delete_author_from_db(author_id, session)
