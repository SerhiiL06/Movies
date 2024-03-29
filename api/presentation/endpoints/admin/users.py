from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from presentation.common.role_cheker import check_role
from presentation.schemes.users.user_schemes import AdminUserScheme, UserCreate
from service.admin.admin_actions import AdminActionService
from service.users.auth import current_user

admin_router = APIRouter(prefix="/admin-route", tags=["admin"])


@admin_router.post("/create-superuser")
@check_role(["admin"])
async def create_superuser(
    user: current_user,
    data: UserCreate,
    service: Annotated[AdminActionService, Depends()],
):
    print("here")
    return await service.create_superuser(data)


@admin_router.get(
    "/users",
    # response_model=List[AdminUserScheme],
)
@check_role(["admin"])
async def get_user_list(
    user: current_user,
    service: Annotated[AdminActionService, Depends()],
    role: str = Query(None, pattern="admin|defaut"),
    is_active: bool = None,
    search: str = None,
    detail: bool = False,
):
    return await service.get_user_list(role=role, active=is_active, email=search)


@admin_router.patch("/users/{user_id}/block")
@check_role(["admin"])
async def block_user(
    user: current_user, user_id: str, service: Annotated[AdminActionService, Depends()]
):
    return await service.block_user(user_id, initiator=user.get("user_id"))


@admin_router.delete("/users/{user_id}/delete")
@check_role(["admin"])
async def delete_user(
    user: current_user, user_id: str, service: Annotated[AdminActionService, Depends()]
):
    return await service.delete_user(user_id, initiator=user.get("user_id"))
