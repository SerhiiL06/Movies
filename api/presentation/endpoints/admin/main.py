from fastapi import APIRouter

from .users import get_user_detail, get_user_list, get_user_movies

admin_router = APIRouter(prefix="/admin", tags=["admin"])


admin_router.add_api_route(path="/users", endpoint=get_user_list)
admin_router.add_api_route(path="/users/{user_id}", endpoint=get_user_detail)
admin_router.add_api_route(path="/users/{user_id}/movies", endpoint=get_user_movies)
