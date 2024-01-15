from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infrastructure.db.models.user import User
from infrastructure.main import async_session
from service.users.user_service import UserService


class AdminActionService:
    def __init__(self) -> None:
        self.crud = UserService()
        self.session = async_session

    async def create_superuser(self, data):
        return await self.crud.register_user(**data, superuser=True)

    async def get_user_list(self, role, active, email, detail):
        async with self.session() as sess:
            query = (
                select(User).options(joinedload(User.movies))
                if detail
                else select(User)
            )

            if role is not None:
                query = query.filter(User.role == role)

            if active is not None:
                query = query.filter(User.is_active == active)

            if email is not None:
                query = query.filter(User.email.icontains(email))

            result = await sess.execute(query)

            return result.unique().scalars().all()

    async def delete_user(self, user_id):
        return await self.crud.delete_user(user_id)
