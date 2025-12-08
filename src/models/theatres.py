import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.actors_and_theatres import ActorsAndTheatres
from src.models.base import Base


class TheatreModel(Base):
    __tablename__ = 'theatres'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=False)

    actors: Mapped[list['ActorModel']] = relationship(
        'ActorModel',
        secondary=ActorsAndTheatres.__table__,
        back_populates='theatres',
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint('name', 'address', name='uq_theatre_name_address'),
    )