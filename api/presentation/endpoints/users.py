from fastapi import APIRouter, Depends
from typing import Annotated

from service.users.user_service import UserService
from service.users.auth import AuthService, current_user

from ..schemes.users.user_schemes import UserCreate
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/users")


@user_router.post("/register", tags=["Auth"])
async def register(user_data: UserCreate, service: UserService = Depends()):
    res = await service.register_user(
        username=user_data.username,
        email=user_data.email,
        password1=user_data.password1,
        password2=user_data.password2,
    )
    return res


@user_router.get("/email-verification/{token}", tags=["Auth"])
async def verify_email(token: str, service: Annotated[UserService, Depends()]):
    return await service.check_email(token)


@user_router.post("/login", tags=["Auth"])
async def login():
    pass


@user_router.post("/token", tags=["Auth"])
async def take_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
):
    return await service.generate_auth_token(data.username, data.password)


@user_router.get("/me", tags=["Profile"])
async def get_profile(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_me(user.get("email"))


@user_router.put("/me", tags=["Profile"])
async def update_profile():
    pass


@user_router.delete("/delete-profile", tags=["Profile"])
async def delete_profile():
    pass


@user_router.post("/change-password", tags=["Password"])
async def change_password():
    pass


@user_router.post("/forgot-password", tags=["Password"])
async def forgot_password():
    pass
