from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from infrastructure.db.models.movie import Category
from service.movies.category_action import CategoryActionService

from ..schemes.category.category_scheme import (
    CreateUpdateCategoryScheme,
    ReadCategoryScheme,
)

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get("", response_model=list[ReadCategoryScheme])
async def read_category_list(service: Annotated[CategoryActionService, Depends()]):
    return await service.read_categories()


@category_router.post("")
async def create_category(
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryActionService, Depends()],
):
    return await service.add_category(data.model_dump())


@category_router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryActionService, Depends()],
):
    return await service.update_category(data, category_id)


@category_router.delete("/{category_id}", response_model=ReadCategoryScheme)
async def delete_category(
    category_id: UUID, service: Annotated[CategoryActionService, Depends()]
):
    return await service.delete_category(category_id)
