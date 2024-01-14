from service.movies.crud_service import CRUDService
from service.movies.user_actions import UserActionsService
from service.users.auth import current_user
from infrastructure.db.models.movie import Movie
from presentation.schemes.movie.movie_schemes import (
    ReadMovieScheme,
    CreateUpdateMovieScheme,
    FilterScheme,
)
from fastapi import Depends, APIRouter
from typing import Annotated, List
from fastapi_filter import FilterDepends
from presentation.schemes.filters import MovieFilter
from typing import Optional
from uuid import UUID


movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get("", response_model=List[ReadMovieScheme])
async def get_movies(
    user: current_user,
    service: Annotated[UserActionsService, Depends()],
    title: str = None,
    viewed: bool = None,
    category: str = None,
):
    result = FilterScheme(title=title, viewed=viewed, category=category).model_dump(
        exclude_none=True
    )
    return await service.get_my_movies(user.get("user_id"), filter_data=result)


@movie_router.post("")
async def create_movie(
    user: current_user,
    data: CreateUpdateMovieScheme,
    service: Annotated[UserActionsService, Depends()],
):
    return await service.add_favorite_movie(data, user.get("user_id"))


@movie_router.delete("/delete/{movie_id}")
async def delete_movie(
    user: current_user,
    movie_id: UUID,
    service: Annotated[UserActionsService, Depends()],
):
    return await service.delete_movie(movie_id, user.get("user_id"))


# @movie_router.put("", response_model=CreateUpdateMovieScheme)
# async def update_movies(user: current_user, service: Annotated[CRUDService, Depends()]):
#     return service.update_model(Movie)
