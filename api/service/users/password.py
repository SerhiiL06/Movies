from passlib.context import CryptContext
from fastapi import HTTPException, status


class PasswordService:
    def __init__(
        self,
    ) -> None:
        self.password = CryptContext(schemes=["bcrypt"])

    def hashed_password(self, pswd) -> str:
        return self.password.hash(pswd)

    def check_password(self, secret, pswd) -> bool:
        return self.password.verify(secret, pswd)

    @staticmethod
    def compare_password(first, second) -> None:
        if first != second:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "400", "message": "Password must be a same"},
            )
