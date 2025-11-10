import uuid

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column, relationship

metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, autoincrement=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())

    profile: Mapped['ProfileModel'] = relationship(
        "Profile",
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )


class ProfileModel(Base):
    __tablename__ = 'profile'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, autoincrement=True, default=uuid.uuid4())
    title: Mapped[str] = mapped_column(sa.String())
    bio: Mapped[str] = mapped_column(sa.String())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["UserModel"] = relationship('user', back_populates='profile')