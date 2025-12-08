import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(sa.String())

    profile: Mapped['ProfileModel'] = relationship(
        "ProfileModel",
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )