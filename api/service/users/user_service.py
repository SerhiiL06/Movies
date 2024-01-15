import codecs
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from infrastructure.db.models.user import User
from infrastructure.main import async_session
from service.email.email_service import EmailService
from service.token.jwt_service import JWTServive

from .password import PasswordService


class UserService:
    def __init__(self):
        self.password = PasswordService()
        self.email = EmailService()
        self.session = async_session
        self.jwt = JWTServive()

    async def register_user(
        self, email, password1, password2, superuser=False, session=async_session()
    ) -> dict:
        try:
            self.password.compare_password(password1, password2)

            hash_password = self.password.hashed_password(password1)

            uuidpk = uuid4()

            user = User(
                id=uuidpk,
                email=email,
                hashed_password=hash_password,
                role="admin" if superuser else "admin",
                is_active=True if superuser else False,
            )

            session.add(user)

            await session.commit()
            if not superuser:
                await self.email.send_email_verification(email)
            return {"code": "200", "message": str(uuidpk)}
        except IntegrityError:
            session.rollback()
            return {"message": "user already exists"}

    async def check_email(self, token):
        data = self.jwt.decode_jwt(token)

        async with self.session() as sess:
            query = (
                update(User)
                .where(User.email == data.get("email"))
                .values(is_active=True)
            )

            res = await sess.execute(query)

            if res.rowcount < 1:
                await sess.rollback()
                raise HTTPException(status_code=400, detail="Wrong data")

            await sess.commit()

            return {"code": "200", "message": "success verify"}

    async def get_me(self, email):
        async with self.session() as sess:
            query = select(User).filter(User.email == email)

            result = await sess.execute(query)

            return result.scalar()

    async def take_token(self, email):
        instance = await self.get_me(email)
        if instance is None:
            raise ValueError({"message": "wrong data"})
        return await self.jwt.create_access_token(instance)

    async def update_profile(self, data, email):
        instance = await self.get_me(email)

        for field, value in data.items():
            setattr(instance, field, value)

        return instance

    async def delete_user(self, user_id):
        async with self.session() as sess:
            instance = await sess.get(User, user_id)
            await sess.delete(instance)
            await sess.commit()
            return {"code": "200", "message": "User delete"}

    async def check_user(self, email, password):
        async with self.session() as sess:
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
