from infrastructure.main import async_session
from infrastructure.db.models.movie import Category
from sqlalchemy import insert, select, update
from uuid import uuid4


class CRUDService:
    def __init__(self):
        self.session = async_session

    async def create_model(self, model, data):
        async with self.session() as sess:
            query = insert(model).values(id=uuid4(), **data.model_dump())
            await sess.execute(query)

            await sess.commit()

        return {"code": "200", "message": "recurs succesfull create"}

    async def read_model(self, model):
        async with self.session() as sess:
            query = select(model)
            result = await sess.execute(query)

            return result.scalars().all()

    async def update_model(self, model, updated_data, object_id):
        async with self.session() as sess:
            model = (
                update(Category)
                .where(model.id == object_id)
                .values(**updated_data.model_dump())
            )

            await sess.execute(model)

            if not model.is_update:
                await sess.rollback()
                return {"message": "something went wrong"}

            await sess.commit()

            return {"message": {"update": object_id}}

    async def delete_model(self, model, object_id):
        async with self.session() as sess:
            model = sess.get(model, object_id)

            await sess.delete(model)
            await sess.commit()

            return {"message": "OK"}
