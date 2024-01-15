from typing import Annotated

from fastapi import Depends, Query

from presentation.common.role_cheker import check_role
from presentation.schemes.users.user_schemes import UserCreate
from service.admin.admin_actions import AdminActionService
from service.users.auth import current_user


@check_role(["admin"])
async def create_superuser(
    user: current_user,
    data: UserCreate,
    service: Annotated[AdminActionService, Depends()],
):
    return await service.create_superuser(data.model_dump())


@check_role(["admin"])
async def get_user_list(
    user: current_user,
    service: Annotated[AdminActionService, Depends()],
    role: str = Query(None, pattern="admin|defaut"),
    is_active: bool = None,
    search: str = None,
    detail: bool = False,
):
    return await service.get_user_list(
        role=role, active=is_active, email=search, detail=detail
    )


@check_role(["admin"])
async def delete_user(
    user: current_user, user_id: str, service: Annotated[AdminActionService, Depends()]
):
    return await service.delete_user(user_id)
