from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from uuid import UUID


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(unique=True, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    birthday: Mapped[datetime] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

    created: Mapped[datetime] = mapped_column(default=func.now())
    is_active: Mapped[bool] = mapped_column(default=False)
