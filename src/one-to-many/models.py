import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declarative_base, DeclarativeMeta

import sqlalchemy as sa


metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class AuthorModel(Base):
    __tablename__ = 'authors'

    id = Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name = Mapped[str] = mapped_column(sa.String())
    last_name = Mapped[str] = mapped_column(sa.String())

    books = Mapped[list['BookModel']] = relationship(
        "BookModel",
        back_populates="authors",
        cascade='all, delete-orphan'
    )


class BookModel(Base):
    __tablename__ = 'books'

    id = Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title = Mapped[str] = mapped_column(sa.String())

    author_id = Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id"))
    author = Mapped["AuthorModel"] = relationship("AuthorModel", back_populates="books")