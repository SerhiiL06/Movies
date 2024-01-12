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

    def generate_auth_token(self, email, password) -> str:
        # await self.user.check_user(email, password)
        return self.jwt.auth(email)


def authenticate(token: str = Depends(bearer)):
    print(token)
    # if token is None:
    #     raise JWTError()
    jwt = JWTServive()

    return jwt.decode_jwt(token)


auth = AuthService()

current_user = Annotated[dict, Depends(authenticate)]
