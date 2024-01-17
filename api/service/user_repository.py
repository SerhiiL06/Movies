from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from infrastructure.db.models.user import User
from .repository import CRUDRepository


class UserRepository(CRUDRepository):
    async def get_me(self, model, user_id):
        async with self.session() as sess:
            query = (
                select(User).where(User.id == user_id).options(joinedload(User.movies))
            )
            result = await sess.execute(query)
            return result.unique().scalars().one()

    async def get_user_by_email(self, email) -> bool:
        async with self.session() as sess:
            query = select(User).where(User.email == email)

            result = await sess.execute(query)
            return result.scalars().one_or_none()

    async def change_password(self, email, pw):
        async with self.session() as sess:
            query = update(User).where(User.email == email).values(hashed_password=pw)

            await sess.execute(query)

            await sess.commit()
