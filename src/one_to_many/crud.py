from sqlalchemy.orm import selectinload

from uuid import UUID

from src.one_to_many.models import AuthorModel, BookModel
from src.one_to_many.schemas import AuthorCreate, AuthorUpdate, AuthorOut

from sqlalchemy import select, delete

from src.exceptions.author import AuthorNotFound

from src.db import SessionDep


async def get_author_from_db(
        author_id: UUID,
        session: SessionDep) -> AuthorOut:
    query = (
        select(AuthorModel)
        .where(AuthorModel.id == author_id)
        .options(selectinload(AuthorModel.books))
    )
    result = await session.execute(query)
    author = result.scalars().first()

    if not author:
        raise AuthorNotFound(author_id=author_id)

    return AuthorOut.model_validate(author)


async def create_author_in_db(
        author: AuthorCreate,
        session: SessionDep) -> AuthorOut:
    new_author = AuthorModel(
        **author.model_dump(exclude={'books'}),
        books=[BookModel(**book.model_dump()) for book in author.books]
    )

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    res = await get_author_from_db(new_author.id, session)

    return res


async def edit_author_in_db(
        author_id: UUID,
        author: AuthorUpdate,
        session: SessionDep) -> AuthorOut:
    query = (
        select(AuthorModel)
        .where(AuthorModel.id == author_id)
        .options(selectinload(AuthorModel.books))
    )
    res = await session.execute(query)

    update_author = res.scalars().first()
    update_author.first_name = author.first_name
    update_author.last_name = author.last_name

    update_author.books = [BookModel(title=book.title) for book in author.books]

    await session.commit()
    res = await get_author_from_db(author_id, session)
    return res


async def delete_book_from_db(author_id: UUID, session: SessionDep):
    query = delete(BookModel).where(BookModel.author_id == author_id)
    await session.execute(query)


async def delete_author_from_db(author_id: UUID, session: SessionDep):
    res = await get_author_from_db(author_id, session)
    await delete_book_from_db(author_id, session)
    query = delete(AuthorModel).where(AuthorModel.id == author_id)
    await session.execute(query)
    return
