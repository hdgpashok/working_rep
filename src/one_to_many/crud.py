from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from uuid import UUID

from src.one_to_many.models import AuthorModel, BookModel
from src.one_to_many.schemas import AuthorCreate, AuthorUpdate, AuthorOut

from sqlalchemy import select

from src.exceptions.author import AuthorNotFound


async def get_author_from_db(
        author_id: UUID,
        session: AsyncSession) -> AuthorOut:
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
        session: AsyncSession) -> AuthorOut:
    new_author = AuthorModel(
        **author.model_dump(exclude={'books'}),
        books=[BookModel(**book.model_dump()) for book in author.books]
    )

    session.add(new_author)
    await session.flush()

    res = await get_author_from_db(new_author.id, session)
    return res


async def edit_author_in_db(
        author_id: UUID,
        author: AuthorUpdate,
        session: AsyncSession) -> AuthorOut:
    query = (
        select(AuthorModel)
        .where(AuthorModel.id == author_id)
        .options(selectinload(AuthorModel.books))
    )
    res = await session.execute(query)

    update_author = res.scalars().one_or_none()

    if not update_author:
        raise AuthorNotFound(author_id=author_id)

    update_author.first_name = author.first_name
    update_author.last_name = author.last_name

    update_author.books = [BookModel(title=book.title) for book in author.books]

    res = await get_author_from_db(author_id, session)
    return res


async def delete_author_from_db(
        author_id: UUID,
        session: AsyncSession):
    author = await session.get(AuthorModel, author_id)
    if not author:
        raise AuthorNotFound(author_id=author_id)

    await session.delete(author)
    return
