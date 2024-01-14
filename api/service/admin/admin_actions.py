from service.users.user_service import UserService
from infrastructure.main import async_session
from infrastructure.db.models.user import User
from sqlalchemy import select


class AdminAction:
    def __init__(self) -> None:
        self.crud = UserService()
        self.session = async_session

    async def create_superuser(self, data):
        return await self.crud.register_user(**data, superuser=True)

    async def get_user_list(self, role, active, email):
        async with self.session() as sess:
            query = select(User)

            if role is not None:
                query = query.filter(User.role == role)

            if active is not None:
                query = query.filter(User.is_active == active)

            if email is not None:
                query = query.filter(User.email.icontains(email))

            result = await sess.execute(query)

            return result.scalars().all()
