import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import BookModel

from src.exceptions.not_found import ObjectNotFound

from src.schemas.books import BookOut, BookCreate, BookUpdate


class BookService:
    @staticmethod
    async def get_book(book_id: UUID, session: AsyncSession) -> BookOut:
        query = (
            select(BookModel)
            .where(book_id == BookModel.id)
        )
        result = await session.execute(query)
        book = result.scalars().first()

        if not book:
            raise ObjectNotFound(object_id=book_id)

        return BookOut.model_validate(book)

    @staticmethod
    async def create_profile(book: BookCreate, session: AsyncSession) -> BookOut:
        new_book = BookModel(
            id=uuid.uuid4(),
            **book.profile.model_dump()
        )
        session.add(new_book)

        return await BookService.get_book(new_book.id, session)

    @staticmethod
    async def update_profile(book_id: UUID, profile: BookUpdate, session: AsyncSession) -> BookOut:
        query = (
            select(BookModel)
            .where(book_id == BookModel.id)
        )
        result = await session.execute(query)

        updated_book = result.scalars().one_or_none()

        if not profile:
            raise ObjectNotFound(object_id=book_id)

        for key, value in profile.model_dump(exclude_unset=True).items():
            setattr(updated_book, key, value)

        return await BookService.get_book(book_id, session)

    @staticmethod
    async def delete_book(book_id: UUID, session: AsyncSession):
        book = await session.get(BookModel, book_id)
        if not book:
            raise ObjectNotFound(object_id=book_id)

        await session.delete(book)
        return
