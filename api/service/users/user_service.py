from infrastructure.main import async_session
from sqlalchemy.exc import IntegrityError
from .password import PasswordService
from infrastructure.db.models.user import User
from uuid import uuid4


class UserService:
    def __init__(self):
        self.password = PasswordService()

    async def register_user(
        self, username, email, password1, password2, session=async_session()
    ):
        try:
            async with session as sess:
                self.password.compare_password(password1, password2)

                hash_password = self.password.hashed_password(password1)

                uuidpk = uuid4()

                user = User(
                    id=uuidpk,
                    username=username,
                    email=email,
                    hashed_password=hash_password,
                )

                sess.add(user)

                await sess.commit()
                return {"code": "200", "message": str(uuidpk)}
        except IntegrityError:
            sess.rollback()
            return {"message": "user already exists"}
