import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.actors_and_theatres import ActorsAndTheatres
from models.theatres import TheatreModel
from src.models.base import Base


class ActorModel(Base):
    __tablename__ = 'actors'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    theatres: Mapped[list["TheatreModel"]] = relationship(
        "TheatreModel",
        secondary=ActorsAndTheatres.__table__,
        back_populates="actors",
        passive_deletes=True
    )