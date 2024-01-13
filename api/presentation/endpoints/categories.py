from service.movies.category_service import CategoryService
from ..schemes.category.category_scheme import (
    CreateUpdateCategoryScheme,
    ReadCategoryScheme,
)
from fastapi import APIRouter, Depends
from uuid import UUID
from typing import Annotated


category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get("", response_model=list[ReadCategoryScheme])
async def read_category_list(service: Annotated[CategoryService, Depends()]):
    return await service.read_categories()


@category_router.post("")
async def create_category(
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryService, Depends()],
):
    return await service.create_category(data)


@category_router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryService, Depends()],
):
    return await service.update_category(data, category_id)


@category_router.delete("/{category_id}", response_model=ReadCategoryScheme)
async def delete_category(
    category_id: UUID, service: Annotated[CategoryService, Depends()]
):
    return await service.delete_category(category_id)
