from src.one_to_many.models import AuthorModel, BookModel
from src.one_to_many.schemas import AuthorCreate

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
