from service.admin.admin_actions import AdminAction
from presentation.common.role_cheker import check_role
from presentation.schemes.users.user_schemes import UserCreate
from service.users.auth import current_user

from fastapi import Depends, Query
from typing import Annotated


@check_role(["admin"])
async def create_superuser(
    user: current_user, data: UserCreate, service: Annotated[AdminAction, Depends()]
):
    return await service.create_superuser(data.model_dump())


@check_role(["admin"])
async def get_user_list(
    user: current_user,
    service: Annotated[AdminAction, Depends()],
    role: str = Query(None, pattern="admin|defaut"),
    is_active: bool = None,
    search: str = None,
):
    return await service.get_user_list(role=role, active=is_active, email=search)


@check_role(["admin"])
async def get_user_movies():
    pass
