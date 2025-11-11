import asyncio
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declarative_base, DeclarativeMeta

import sqlalchemy as sa

from src.one_to_one.models import create_database_tables, Base


class AuthorModel(Base):
    __tablename__ = 'authors'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(sa.String())
    last_name: Mapped[str] = mapped_column(sa.String())

    books: Mapped[list['BookModel']] = relationship(
        "BookModel",
        back_populates="author",
        cascade='all, delete-orphan'
    )


class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(sa.String())

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["AuthorModel"] = relationship("AuthorModel", back_populates="books")


if __name__ == '__main__':
    asyncio.run(create_database_tables())