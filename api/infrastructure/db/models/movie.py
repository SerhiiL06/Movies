from typing import List

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, create, idpk


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[create]

    movies: Mapped[List["Movie"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return self.title


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)

    created_at: Mapped[create]
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )

    viewed: Mapped[bool] = mapped_column(default=True)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    category: Mapped["Category"] = relationship(back_populates="movies")

    owner: Mapped["User"] = relationship(back_populates="movies")

    def __repr__(self) -> str:
        return self.title
