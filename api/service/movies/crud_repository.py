from uuid import uuid4

from sqlalchemy import delete, insert, select, update
from service.repository import AbstractRepository

from infrastructure.main import async_session


class CRUDRepository(AbstractRepository):
    def __init__(self):
        self.session = async_session

    async def create_model(self, model, data):
        async with self.session() as sess:
            query = insert(model).values(id=uuid4(), **data).returning(model.id)
            await sess.execute(query)

            await sess.commit()

        return query.is_insert

    async def read_model(self, model, filter_data):
        async with self.session() as sess:
            query = select(model).filter_by(**filter_data)
            result = await sess.execute(query)

            return result.scalars().all()

    async def update_model(self, model, data, object_id):
        async with self.session() as sess:
            model = update(model).where(model.id == object_id).values(**data)

            await sess.execute(model)

            await sess.commit()

            return {"message": {"update": object_id}}

    async def delete_model(self, model, object_id):
        async with self.session() as sess:
            query = delete(model).where(model.id == object_id)

            await sess.execute(query)
            await sess.commit()

            return {"message": "OK"}
