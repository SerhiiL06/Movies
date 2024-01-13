from service.movies.crud_service import CRUDService
from infrastructure.db.models.movie import Category
from ..schemes.category.category_scheme import (
    CreateUpdateCategoryScheme,
    ReadCategoryScheme,
)
from fastapi import APIRouter, Depends
from uuid import UUID
from typing import Annotated


category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get("", response_model=list[ReadCategoryScheme])
async def read_category_list(service: Annotated[CRUDService, Depends()]):
    return await service.read_model(Category)


@category_router.post("")
async def create_category(
    data: CreateUpdateCategoryScheme, service: Annotated[CRUDService, Depends()]
):
    return await service.create_model(Category, data)


@category_router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    data: CreateUpdateCategoryScheme,
    service: Annotated[CRUDService, Depends()],
):
    return await service.update_model(Category, data, category_id)


@category_router.delete("/{category_id}", response_model=ReadCategoryScheme)
async def delete_category(
    category_id: UUID, service: Annotated[CRUDService, Depends()]
):
    return await service.delete_model(Category, category_id)
