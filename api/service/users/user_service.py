from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import update
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
