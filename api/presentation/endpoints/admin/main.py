from fastapi import APIRouter
from typing import List

from .users import get_user_list, create_superuser, get_user_movies
from presentation.schemes.users.user_schemes import AdminUserScheme

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
admin_router.add_api_route(path="/users/{user_id}/movies", endpoint=get_user_movies)
