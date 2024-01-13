from infrastructure.main import async_session
from infrastructure.db.models.movie import Category
from sqlalchemy import insert, select, update
from uuid import uuid4


class CategoryService:
    def __init__(self) -> None:
        pass

    async def create_category(self, data, session=async_session):
        async with session() as sess:
            query = insert(Category).values(id=uuid4(), title=data.title)
            await sess.execute(query)

            await sess.commit()

        return {"code": "200", "message": "category succesfull create"}

    async def read_categories(self, session=async_session):
        async with session() as sess:
            query = select(Category)
            result = await sess.execute(query)

            return result.scalars().all()

    async def update_category(self, updated_data, category_id, session=async_session):
        async with session() as sess:
            category = (
                update(Category)
                .where(Category.id == category_id)
                .values(**updated_data.model_dump())
            )

            await sess.execute(category)

            if not category.is_update:
                await sess.rollback()
                return {"message": "something went wrong"}

            await sess.commit()

            return {"message": {"update": category_id}}

    async def delete_category(self, category_id, session=async_session):
        async with session() as sess:
            category = sess.get(Category, category_id)

            await sess.delete(category)
            await sess.commit()
