import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.one_to_one.models import Base


class ActorsAndTheatres(Base):
    __tablename__ = 'actors_and_theatres'

    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actors.id", ondelete='CASCADE'),
        primary_key=True,

    )
    theatre_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("theatres.id", ondelete='CASCADE'),
        primary_key=True
    )

