import asyncio
import uuid

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column, relationship

from db import engine

metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())

    profile: Mapped['ProfileModel'] = relationship(
        "ProfileModel",
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )


class ProfileModel(Base):
    __tablename__ = 'profile'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())
    bio: Mapped[str] = mapped_column(sa.String())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["UserModel"] = relationship('UserModel', back_populates='profile')


async def create_database_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("success init")
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(create_database_tables())
