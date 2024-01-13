from .crud_service import CRUDService
from infrastructure.main import async_session
from infrastructure.db.models.movie import Movie, Category

from sqlalchemy import insert, select
from sqlalchemy.orm import lazyload, joinedload
from uuid import uuid4
from fastapi import HTTPException, status


class UserActionsService:
    INSTANCE = Movie

    def __init__(self) -> None:
        self.crud = CRUDService()
        self.session = async_session

    async def add_favorite_movie(self, data, owner):
        async with self.session() as sess:
            query = insert(self.INSTANCE).values(
                id=uuid4(), **data.model_dump(), owner_id=owner
            )

            result = await sess.execute(query)

            if not result.is_insert:
                await sess.rollback()
                return {"code": "400", "message": "something went wrong"}

            await sess.commit()
            return {"code": "200", "message": "movie was added"}

    async def get_my_movies(self, owner, filter_data=None):
        async with self.session() as sess:
            query = (
                select(self.INSTANCE)
                .where(self.INSTANCE.owner_id == owner)
                .filter(
                    (self.INSTANCE.title).contains(filter_data if filter_data else "")
                )
                .options(joinedload(self.INSTANCE.category))
            )

            result = await sess.execute(query)

            return result.scalars().all()

    async def delete_movie(self, movie_id, owner):
        async with self.session() as sess:
            instance = await sess.get(self.INSTANCE, movie_id)

            if str(instance.owner_id) != owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"code": "403", "message": "for"},
                )

            await sess.delete(instance)

            await sess.commit()