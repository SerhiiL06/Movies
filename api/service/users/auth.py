from ..token.jwt_service import JWTServive
from typing import Annotated
from .user_service import UserService
from fastapi import Depends
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer


bearer = OAuth2PasswordBearer(tokenUrl="users/token")


class AuthService:
    def __init__(self) -> None:
        self.jwt = JWTServive()
        self.user = UserService()

    def authenticate(self, token: str = Depends(bearer)):
        if token is None:
            raise JWTError()

        return self.jwt.decode_jwt(token)


auth = AuthService()

current_user = Annotated[dict, Depends(auth.authenticate)]
