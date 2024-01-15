from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryScheme(BaseModel):
    title: str


class CreateUpdateCategoryScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str


class ReadCategoryScheme(CreateUpdateCategoryScheme):
    id: UUID
    created_at: date
