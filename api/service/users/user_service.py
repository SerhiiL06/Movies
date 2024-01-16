import codecs
from uuid import uuid4

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from infrastructure.db.models.user import User
from service.email.email_service import EmailService
from service.token.jwt_service import JWTServive
from service.UserRepository import UserRepository

from .password import PasswordService


class VerificationServiceMixin:
    def __init__(self):
        self.password = PasswordService()
        self.jwt = JWTServive()

    async def verify_email_and_password(self, email, password):
        user_instance = await self.crud.get_user_by_email(self.INSTANCE, email)

        if user_instance is None:
            raise HTTPException(status_code=400, detail={"message": "wrong data"})

        self.password.check_password(password, user_instance.hashed_password)

        return user_instance

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


class UserService(VerificationServiceMixin):
    INSTANCE = User

    def __init__(self, crud: UserRepository = Depends()):
        self.password = PasswordService()
        self.email = EmailService()
        self.crud = crud
        self.jwt = JWTServive()

    async def register_user(self, data) -> dict:
        self.password.compare_password(data.password1, data.password2)

        hashed_pw = self.password.hashed_password(data.password1)

        user_data = data.model_dump(exclude=["password1", "password2"])
        user_data.update({"hashed_password": hashed_pw, "role": "default"})

        result = await self.crud.create_model(self.INSTANCE, user_data)

        if result is True:
            await self.email.send_email_verification(data.email)

        return {"message": "OK"}

    async def update_profile(self, data, user_id):
        msg = await self.crud.update_model(self.INSTANCE, data, user_id)
        return msg

    async def delete_user(self, user_id):
        msg = self.crud.delete_model(self.INSTANCE, user_id)
        return {"code": "200", "message": msg}

    async def get_me(self, user_id):
        return await self.crud.get_me(self.INSTANCE, user_id)

    async def take_token(self, email, password):
        instance = await self.verify_email_and_password(email, password)
        return await self.jwt.create_access_token(instance)
