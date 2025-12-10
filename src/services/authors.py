import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.exceptions.not_found import ObjectNotFound

from src.models.books import BookModel
from src.models.authors import AuthorModel

from src.schemas.authors import AuthorOut, AuthorCreate, AuthorUpdate


class AuthorRepository:
    @staticmethod
    async def get_author_from_db(author_id: UUID, session: AsyncSession) -> AuthorOut:
        query = (
            select(AuthorModel)
            .filter(author_id == AuthorModel.id)
            .options(selectinload(AuthorModel.books))
        )
        result = await session.execute(query)
        author = result.scalars().first()

        if not author:
            raise ObjectNotFound(object_id=author_id)

        return AuthorOut.model_validate(author)

    @staticmethod
    async def create_author_in_db(author: AuthorCreate, session: AsyncSession) -> AuthorOut:
        new_author = AuthorModel(
            id=uuid.uuid4(),
            **author.model_dump(exclude={'books'}),
            books=[BookModel(**book.model_dump()) for book in author.books]
        )

        session.add(new_author)

        return await AuthorRepository.get_author_from_db(new_author.id, session)

    @staticmethod
    async def edit_author_in_db(author_id: UUID, author: AuthorUpdate, session: AsyncSession) -> AuthorOut:
        query = (
            select(AuthorModel)
            .filter(author_id == AuthorModel.id)
            .options(selectinload(AuthorModel.books))
        )
        res = await session.execute(query)

        update_author = res.scalars().one_or_none()

        if not update_author:
            raise ObjectNotFound(object_id=author_id)

        for key, value in author.model_dump(exclude={'books'}, exclude_unset=True).items():
            setattr(update_author, key, value)

        update_author.books = [BookModel(title=book.title) for book in author.books]

        return await AuthorRepository.get_author_from_db(author_id, session)

    @staticmethod
    async def delete_author_from_db(author_id: UUID, session: AsyncSession):
        author = await session.get(AuthorModel, author_id)
        if not author:
            raise ObjectNotFound(object_id=author_id)

        await session.delete(author)
        return