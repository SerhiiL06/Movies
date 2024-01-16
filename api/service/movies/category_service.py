from fastapi import Depends

from infrastructure.db.models.movie import Category


from service.repository import CRUDRepository


class CategoryActionService:
    INSTANCE = Category

    def __init__(self, crud: CRUDRepository = Depends()) -> None:
        self.crud = crud

    async def add_category(self, data):
        await self.crud.create_model(self.INSTANCE, data)

    async def read_categories(self):
        return await self.crud.read_model(self.INSTANCE, filter_data={})

    async def update_category(self, data, category_id):
        data = data.model_dump(exclude_none=True)
        await self.crud.update_model(self.INSTANCE, data, category_id)

    async def delete_category(self, category_id):
        return await self.crud.delete_model(self.INSTANCE, category_id)
