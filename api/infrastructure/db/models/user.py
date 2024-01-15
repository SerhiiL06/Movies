from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .movie import Movie


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(unique=True, primary_key=True, default=uuid4())
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str]

    hashed_password: Mapped[str]

    birthday: Mapped[datetime] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

    created: Mapped[datetime] = mapped_column(default=func.now())
    is_active: Mapped[bool] = mapped_column(default=False)

    movies: Mapped[List["Movie"]] = relationship(back_populates="owner")
