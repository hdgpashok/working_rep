import asyncio
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.one_to_one.models import create_database_tables, Base


class ActorModel(Base):
    __tablename__ = 'actors'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    theatres: Mapped[list["TheatreModel"]] = relationship(
        "TheatreModel",
        secondary='actors_and_theatres',
        back_populates="actors",
        cascade='save-update'
    )


class TheatreModel(Base):
    __tablename__ = 'theatres'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=False)

    actors: Mapped[list['ActorModel']] = relationship(
        'ActorModel',
        secondary="actors_and_theatres",
        back_populates='theatres'
    )

    __table_args__ = (
        UniqueConstraint('name', 'address', name='uq_theatre_name_address'),
    )


class ActorsAndTheatres(Base):
    __tablename__ = 'actors_and_theatres'

    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(ActorModel.id), primary_key=True)
    theatre_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(TheatreModel.id), primary_key=True)


if __name__ == '__main__':
    asyncio.run(create_database_tables())