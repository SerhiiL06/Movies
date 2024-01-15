import codecs

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select, update

from infrastructure.db.models.user import User
from infrastructure.db.redis import RedisTools
from infrastructure.main import async_session


class PasswordService:
    def __init__(
        self,
    ) -> None:
        self.session = async_session
        self.crypt = CryptContext(schemes=["bcrypt"])

    def hashed_password(self, pswd) -> str:
        return self.crypt.hash(pswd)

    def check_password(self, secret, pswd) -> bool:
        verify = self.crypt.verify(secret, pswd)

        if not verify:
            raise HTTPException(status_code=403, detail="email or password was wrong")

    async def change_password(
        self,
        data,
        email,
        with_code=False,
    ):
        self.crypt.compare_password(data.password1, data.password2)
        async with self.session() as sess:
            instance = await self.get_me(email)

            if not with_code:
                self.crypt.check_password(data.password1, instance.hashed_password)

            to_change = data.password1 if with_code else data.new_password
            new = self.crypt.hashed_password(to_change)

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

    @staticmethod
    def compare_password(first, second) -> None:
        if first != second:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "400", "message": "Password must be a same"},
            )
