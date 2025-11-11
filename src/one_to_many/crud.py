from sqlalchemy.orm import selectinload

from uuid import UUID

from src.one_to_many.models import AuthorModel, BookModel
from src.one_to_many.schemas import AuthorCreate, AuthorRead, AuthorOut, AuthorEdit

from sqlalchemy import select, delete

from fastapi import HTTPException

from src.db import SessionDep


async def create_author_in_db(author: AuthorCreate, session: SessionDep):
    new_author = AuthorModel(
        first_name=author.first_name,
        last_name=author.last_name,
        books= [BookModel(title=book.title) for book in author.books]
    )

    session.add(new_author)
    await session.commit()

    return {'status': 'author created'}


async def get_author_from_db(author_id: UUID, session: SessionDep):
    query = select(AuthorModel).where(AuthorModel.id == author_id).options(selectinload(AuthorModel.books))
    result = await session.execute(query)

    return result.scalars().first()


async def edit_author_in_db(author_id: UUID, author: AuthorEdit, session: SessionDep):
    query = select(AuthorModel).where(AuthorModel.id == author_id).options(selectinload(AuthorModel.books))
    result = await session.execute(query)

    update_author = result.scalars().first()

    if not update_author:
        raise HTTPException(status_code=404, detail="author not found")

    update_author.first_name = author.first_name
    update_author.last_name = author.last_name

    update_author.books = [BookModel(title=book.title) for book in author.books]

    return {'status': 'user edited'}


async def delete_book_from_db(author_id: UUID, session: SessionDep):
    query = delete(BookModel).where(BookModel.author_id == author_id)
    await session.execute(query)


async def delete_author_from_db(author_id: UUID, session: SessionDep):
    await delete_book_from_db(author_id, session)
    query = delete(AuthorModel).where(AuthorModel.id == author_id)
    await session.execute(query)
