from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional, Any
from datetime import date
from ..category.category_scheme import CreateUpdateCategoryScheme


class CreateUpdateMovieScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=250)

    rating: int = Field(gt=0, lte=5)

    category_id: UUID4


class ReadMovieScheme(BaseModel):
    id: UUID4
    title: str
    description: str

    rating: Optional[int] = None
    # created_at: date = Field(serialization_alias="created")

    category: CreateUpdateCategoryScheme


class FilterScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None
    viewed: bool | None
    category: str | None
