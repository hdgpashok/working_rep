import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.many_to_many.models.actors_and_theatres import ActorsAndTheatres
from src.many_to_many.models.theatres import TheatreModel
from src.one_to_one.models import Base


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