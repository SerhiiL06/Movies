import codecs

from fastapi import HTTPException, status
from passlib.context import CryptContext
from service.email.email_service import EmailService

from infrastructure.db.models.user import User
from infrastructure.db.redis import RedisTools
from infrastructure.main import async_session


class PasswordService:
    def __init__(
        self,
    ) -> None:
        self.session = async_session
        self.email = EmailService()
        self.crypt = CryptContext(schemes=["bcrypt"])

    def hashed_password(self, pswd) -> str:
        return self.crypt.hash(pswd)

    def check_password(self, secret, pswd) -> bool:
        verify = self.crypt.verify(secret, pswd)

        if not verify:
            raise HTTPException(status_code=403, detail="email or password was wrong")

    async def forgot_password(self, email):
        code = await self.email.send_confirm_code(email)

        redis = RedisTools()
        await redis.set_value(code, email)

        return {"code": "200", "message": "email was sent"}

    async def set_password_with_code(self, data) -> str:
        redis = RedisTools()

        email = await redis.get_value(data.code)

        if email is None:
            raise HTTPException(
                status_code=400,
                detail={"code": "404", "message": "invalid or expired code. Try again"},
            )

        await redis.del_value(data.code)

        return codecs.decode(email, encoding="utf-8")

    @staticmethod
    def compare_password(first, second) -> None:
        if first != second:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "400", "message": "Password must be a same"},
            )
