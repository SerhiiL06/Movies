from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends

from presentation.schemes.movie.movie_schemes import (
    CreateUpdateMovieScheme,
    FilterScheme,
    ReadMovieScheme,
)
from service.movies.movie_action import MovieActionsService
from service.users.auth import current_user

from ..schemes.movie.movie_schemes import CreateUpdateMovieScheme

movie_router = APIRouter(prefix="/movie", tags=["Movies"])


@movie_router.get("", response_model=List[ReadMovieScheme])
async def get_movies(
    user: current_user,
    service: Annotated[MovieActionsService, Depends()],
    title: str = None,
    viewed: bool = None,
    category: str = None,
):
    result = FilterScheme(
        title=title, owner_id=user.get("user_id"), viewed=viewed, category=category
    ).model_dump(exclude_none=True)
    return await service.get_my_movies(result)


@movie_router.post("/create")
async def create_movie(
    user: current_user,
    data: CreateUpdateMovieScheme,
    service: Annotated[MovieActionsService, Depends()],
):
    result = await service.add_favorite_movie(
        data.model_dump(), owner=user.get("user_id")
    )

    return result


@movie_router.put("/update/{movie_id}")
async def update_movies(
    user: current_user,
    movie_id: str,
    data: CreateUpdateMovieScheme,
    service: Annotated[MovieActionsService, Depends()],
):
    return await service.update_movie(data, movie_id)


@movie_router.delete("/delete/{movie_id}")
async def delete_movie(
    user: current_user,
    movie_id: UUID,
    service: Annotated[MovieActionsService, Depends()],
):
    return await service.delete_movie(movie_id)
