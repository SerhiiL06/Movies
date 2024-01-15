from fastapi import Depends

from infrastructure.db.models.movie import Movie


from .crud_repository import CRUDRepository


class MovieActionsService:
    INSTANCE = Movie

    def __init__(self, crud: CRUDRepository = Depends()) -> None:
        self.crud = crud

    async def add_favorite_movie(self, data, owner, wishlist=False):
        data_to_save = {**data, "owner_id": owner, "viewed": wishlist}
        result = await self.crud.create_model(model=self.INSTANCE, data=data_to_save)

        return {"code": "200", "message": result}

    async def get_my_movies(self, filter_data):
        return await self.crud.read_model(self.INSTANCE, filter_data)

    async def update_movie(self, data, movie_id):
        data = data.model_dump(exclude_none=True)
        return await self.crud.update_model(self.INSTANCE, data, movie_id)

    async def delete_movie(self, movie_id):
        return await self.crud.delete_model(model=self.INSTANCE, object_id=movie_id)
