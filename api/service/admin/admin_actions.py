from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infrastructure.db.models.user import User
from service.repository import CRUDRepository
from service.users.password import PasswordService
from fastapi import Depends
from presentation.schemes.users.user_schemes import UserFilterSchema


class AdminActionService:
    INSTANCE = User

    def __init__(self, crud: CRUDRepository = Depends()) -> None:
        self.crud = crud
        self.password = PasswordService()

    async def create_superuser(self, data: dict):
        self.password.compare_password(data.password1, data.password2)
        hash_pw = self.password.hashed_password(data.password1)
        format_in_dict = data.model_dump(exclude=["password1", "password2"])
        format_in_dict.update(
            {"hashed_password": hash_pw, "is_active": True}, {"role": "admin"}
        )

        return await self.crud.create_model(self.INSTANCE, format_in_dict)

    async def get_user_list(self, role, active, email, detail):
        filter_data = UserFilterSchema(
            email=email, role=role, is_active=active
        ).model_dump(exclude_none=True)
        return await self.crud.read_model(self.INSTANCE, filter_data)

    async def delete_user(self, user_id):
        return await self.crud.delete_model(self.INSTANCE, user_id)
