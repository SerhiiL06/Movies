from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from presentation.common.role_cheker import check_role
from presentation.schemes.category.category_scheme import (
    CreateUpdateCategoryScheme, ReadCategoryScheme)
from service.movies.category_service import CategoryActionService
from service.users.auth import current_user

category_router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@category_router.get("", response_model=list[ReadCategoryScheme])
@check_role(["admin"])
async def category_list(
    user: current_user, service: Annotated[CategoryActionService, Depends()]
):
    return await service.read_categories()


@category_router.post("")
@check_role(["admin"])
async def create_category(
    user: current_user,
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryActionService, Depends()],
):
    return await service.add_category(data)


@category_router.put("/{category_id}", status_code=status.HTTP_200_OK)
@check_role(["admin"])
async def update_category(
    user: current_user,
    category_id: UUID,
    data: CreateUpdateCategoryScheme,
    service: Annotated[CategoryActionService, Depends()],
):
    return await service.update_category(data, category_id)


@category_router.delete("/{category_id}")
@check_role(["admin"])
async def delete_category(
    user: current_user,
    category_id: UUID,
    service: Annotated[CategoryActionService, Depends()],
):
    return await service.delete_category(category_id)
