from fastapi import Depends
from presentation.schemes.movie.movie_schemes import ReadMovieScheme
from service.exceptions import PermissionDenied
from infrastructure.db.models.movie import Movie
from service.repository import CRUDRepository


class MovieActionsService:
    INSTANCE = Movie

    def __init__(self, crud: CRUDRepository = Depends()) -> None:
        self.crud = crud

    async def add_favorite_movie(self, data, owner):
        format_data = data.model_dump(exclude_none=True)
        format_data.update({"owner_id": owner})
        result = await self.crud.create_model(model=self.INSTANCE, data=format_data)

        return {"detail": {"code": "201", "msg": "SUCCESS", "objectId": result}}

    async def get_my_movies(self, filter_data):
        to_filter = filter_data.model_dump(exclude_none=True)
        return await self.crud.read_model(self.INSTANCE, to_filter)

    async def update_movie(self, data, user_id, movie_id):
        data = data.model_dump(exclude_none=True)

        current_obj_id = await self.crud.get_owner(self.INSTANCE, movie_id)
        if str(current_obj_id) != user_id:
            raise PermissionDenied()
        result = await self.crud.update_model(self.INSTANCE, data, movie_id)

        return {"detail": {"code": "200", "msg": "UPDATE", "objectId": result}}

    async def delete_movie(self, movie_id):
        return await self.crud.delete_model(model=self.INSTANCE, object_id=movie_id)
