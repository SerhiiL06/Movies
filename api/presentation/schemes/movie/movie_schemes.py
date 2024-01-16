from datetime import date
from typing import Any, Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

from ..category.category_scheme import CreateUpdateCategoryScheme


class CreateUpdateMovieScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_to_lower=True)

    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=250)

    rating: Optional[int] = Field(None, gt=0, lte=5)

    category_id: Optional[UUID4] = None


class ReadMovieScheme(BaseModel):
    id: UUID4
    title: str
    description: str

    rating: Optional[int] = None


class FilterScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None
    viewed: bool | None
    owner_id: UUID4
    category: str | None
