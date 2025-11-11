from sqlalchemy.orm import selectinload

from uuid import UUID

from src.one_to_many.models import AuthorModel, BookModel
from src.one_to_many.schemas import AuthorCreate, AuthorRead, AuthorOut

from sqlalchemy import select

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


async def get_author_in_db(author_id: UUID, session: SessionDep):
    query = select(AuthorModel).where(AuthorModel.id == author_id).options(selectinload(AuthorModel.books))
    result = await session.execute(query)

    return result.scalars().first()