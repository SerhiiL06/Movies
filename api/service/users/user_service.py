from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError

from infrastructure.db.models.user import User
from infrastructure.main import async_session
from service.email.email_service import EmailService
from service.token.jwt_service import JWTServive

from .password import PasswordService

from .password import PasswordService


class UserService:
    def __init__(self):
        self.password = PasswordService()
        self.email = EmailService()
        self.jwt = JWTServive()

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
                    role="default",
                )

                sess.add(user)

                await sess.commit()
                await self.email.send_email_verification(email)
                return {"code": "200", "message": str(uuidpk)}
        except IntegrityError:
            sess.rollback()
            return {"message": "user already exists"}

    async def check_email(self, token, session=async_session()):
        email = self.jwt.decode_jwt(token)

        async with session as sess:
            query = update(User).where(User.email == email).values(is_active=True)

            res = await sess.execute(query)

            if res.rowcount < 1:
                await sess.rollback()
                raise HTTPException(status_code=400, detail="Wrong data")

            await sess.commit()

            return {"code": "200", "message": "success verify"}

    async def get_me(self, user_id, session=async_session()):
        async with session as sess:
            return await sess.get(User, user_id)

    async def take_token(self, email):
        instance = await self.get_me(email)
        return await self.jwt.create_access_token(instance)

    async def update_profile(self, data, email):
        instance = await self.get_me(email)

        for field, value in data.items():
            setattr(instance, field, value)

        return instance

    async def delete_user(self, user_id):
        pass

    async def check_user(self, email, password, session=async_session()):
        async with session as sess:
            res = await sess.execute(select(User).where(User.email == email))
            user_instance = res.scalar()

            error_pack = []

            if user_instance is None:
                error_pack.append(
                    {"code": "404", "message": "email or password was wrong"}
                )

            if user_instance and user_instance.is_active == False:
                error_pack.append({"code": "403", "message": "verify your profile"})

            if error_pack:
                raise HTTPException(status_code=400, detail=error_pack)

            self.password.check_password(password, user_instance.hashed_password)
