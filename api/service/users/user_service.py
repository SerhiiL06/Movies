import codecs
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from infrastructure.db.models.user import User
from infrastructure.db.redis import RedisTools
from infrastructure.main import async_session
from service.email.email_service import EmailService
from service.token.jwt_service import JWTServive

from .password import PasswordService


class UserService:
    def __init__(self):
        self.password = PasswordService()
        self.email = EmailService()
        self.jwt = JWTServive()

    async def register_user(self, email, password1, password2, session=async_session()):
        try:
            self.password.compare_password(password1, password2)

            hash_password = self.password.hashed_password(password1)

            uuidpk = uuid4()

            user = User(
                id=uuidpk,
                email=email,
                hashed_password=hash_password,
                role="default",
            )

            session.add(user)

            await session.commit()
            await self.email.send_email_verification(email)
            return {"code": "200", "message": str(uuidpk)}
        except IntegrityError:
            session.rollback()
            return {"message": "user already exists"}

    async def check_email(self, token, session=async_session()):
        data = self.jwt.decode_jwt(token)

        async with session as sess:
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

    async def get_me(self, email, session=async_session()):
        query = select(User).filter(User.email == email)

        result = await session.execute(query)

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

    async def delete_user(self, user_id, session=async_session()):
        instance = await session.get(User, user_id)
        await session.delete(instance)
        await session.commit()
        return {"code": "200", "message": "User delete"}

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

    async def change_password(
        self,
        data,
        email,
        with_code=False,
        session=async_session(),
    ):
        self.password.compare_password(data.password1, data.password2)
        async with session as sess:
            instance = await self.get_me(email)

            if not with_code:
                self.password.check_password(data.password1, instance.hashed_password)

            to_change = data.password1 if with_code else data.new_password
            new = self.password.hashed_password(to_change)

            query = (
                update(User)
                .where(User.email == instance.email)
                .values(hashed_password=new)
            )

            await sess.execute(query)

            await sess.commit()

    async def forgot_password(self, email):
        instance = await self.get_me(email)
        if instance is None:
            raise HTTPException(
                status_code=400,
                detail={"code": "400", "message": "user with this email doesnt exists"},
            )

        code = await self.email.send_confirm_code(email)

        redis = RedisTools()
        await redis.set_value(code, email)

        return {"code": "200", "message": "email was sent"}

    async def set_password_with_code(self, data):
        redis = RedisTools()

        email = await redis.get_value(data.code)

        if email is None:
            raise HTTPException(
                status_code=400,
                detail={"code": "404", "message": "invalid or expired code. Try again"},
            )

        await self.change_password(
            data, codecs.decode(email, encoding="utf-8"), with_code=True
        )

        await redis.del_value(data.code)
