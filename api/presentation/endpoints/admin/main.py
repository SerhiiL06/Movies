from typing import List

from fastapi import APIRouter

from presentation.schemes.users.user_schemes import AdminUserScheme

from .users import create_superuser, delete_user, get_user_list

admin_router = APIRouter(prefix="/admin", tags=["admin"])


admin_router.add_api_route(
    path="/create-superuser", endpoint=create_superuser, methods=["post"]
)
admin_router.add_api_route(
    path="/users",
    endpoint=get_user_list,
    response_model=List[AdminUserScheme],
    methods=["get"],
)
admin_router.add_api_route(path="/users/{user_id}/delete", endpoint=delete_user)
