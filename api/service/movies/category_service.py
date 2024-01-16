from typing import Literal

from fastapi import Depends

from infrastructure.db.models.movie import Category
from service.exceptions import ObjectDoesntExists
from service.repository import CRUDRepository


class CategoryActionService:
    INSTANCE = Category

    def __init__(self, crud: CRUDRepository = Depends()) -> None:
        self.crud = crud

    async def add_category(self, data):
        result = await self.crud.create_model(self.INSTANCE, data.model_dump())
        return self.default_return("create", result)

    async def read_categories(self):
        return await self.crud.read_model(self.INSTANCE, filter_data={})

    async def update_category(self, data, category_id):
        data = data.model_dump(exclude_none=True)
        result = await self.crud.update_model(self.INSTANCE, data, category_id)
        return self.default_return("update", result)

    async def delete_category(self, category_id):
        result = await self.crud.delete_model(self.INSTANCE, category_id)

        if not result:
            raise ObjectDoesntExists(self.INSTANCE)

        return {"detail": {"code": "204", "message": "delete success"}}

    @classmethod
    def default_return(cls, action: Literal["create", "update"], obj_id: int) -> dict:
        return {
            "detail": {
                "code": "200",
                "msg": f"object success {action}",
                "objectId": obj_id,
            }
        }
