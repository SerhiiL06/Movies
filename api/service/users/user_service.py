from uuid import uuid4

from fastapi import Depends, HTTPException, BackgroundTasks
from sqlalchemy import update
from service.exceptions import ObjectDoesntExists
from infrastructure.db.models.user import User
from service.email.email_service import EmailService
from service.token.jwt_service import JWTServive
from service.user_repository import UserRepository
from service.exceptions import UserAlreadyExists
from .password import PasswordService
from service.users.password import PasswordService


class VerificationServiceMixin:
    def __init__(self):
        self.password = PasswordService()
        self.jwt = JWTServive()

    async def verify_email_and_password(self, email, password):
        user_instance = await self.crud.get_user_by_email(email)

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
        user_instance = await self.crud.get_user_by_email(data.email)
        if user_instance:
            raise UserAlreadyExists(data.email)
        self.password.compare_password(data.password1, data.password2)

        hashed_pw = self.password.hashed_password(data.password1)

        user_data = data.model_dump(exclude=["password1", "password2"])
        user_data.update({"hashed_password": hashed_pw, "role": "default"})

        result = await self.crud.create_model(user_data)
        task = BackgroundTasks()
        task.add_task(self.email.send_email_verification, data.email)

        return {"code": "201", "msg": "create successfull", "objectId": result}

    async def forgot_password(self, email):
        user_exists = await self.crud.get_user_by_email(email)

        if not user_exists:
            raise ObjectDoesntExists(self.INSTANCE)

        return await self.password.forgot_password(email)

    async def set_password_with_code(self, data):
        email = await self.password.set_password_with_code(data)

        await self.change_password(data, email, with_code=True)

        return {"code": "200", "detail": {"msg": "SET PASSWORD"}}

    async def change_password(self, data, email, with_code=None):
        if not with_code:
            self.password.compare_password(data.password1, data.password2)
            await self.verify_email_and_password(email, data.password1)

        pw = self.password.hashed_password(
            data.password1 if with_code else data.new_password
        )
        await self.crud.change_password(email, pw)

    async def update_profile(self, data, user_id):
        obj = await self.crud.update_model(
            self.INSTANCE, data.model_dump(exclude_none=True), user_id
        )
        return {"code": "200", "detail": {"msg": "UPDATE", "objectId": obj[0]}}

    async def delete_user(self, user_id):
        msg = self.crud.delete_model(self.INSTANCE, user_id)
        return {"code": "200", "message": msg}

    async def get_me(self, user_id):
        result = await self.crud.get_me(self.INSTANCE, user_id)

        return result

    async def take_token(self, email, password):
        instance = await self.verify_email_and_password(email, password)
        return await self.jwt.create_access_token(instance)
