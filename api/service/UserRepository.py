from sqlalchemy import select

from .repository import CRUDRepository


class UserRepository(CRUDRepository):
    async def get_me(self, model, user_id):
        async with self.session() as sess:
            current_user = await sess.get(model, user_id)

            return current_user

    async def get_user_by_email(self, model, email):
        async with self.session() as sess:
            query = select(model).where(model.email == email)

            result = await sess.execute(query)
            return result.scalars().one_or_none()
