from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import EmailStr

from service.users.auth import current_user
from service.users.user_service import UserService

from ..schemes.users.password_schemes import (
    ChangePasswordScheme,
    ChangePasswordWithCode,
)
from ..schemes.users.user_schemes import UpdateUser, UserCreate, UserProfile

user_router = APIRouter(prefix="/users")


@user_router.post("/register", tags=["Auth"])
async def register(user_data: UserCreate, service: UserService = Depends()):
    return await service.register_user(user_data)


@user_router.get("/email-verification/{token}", tags=["Auth"])
async def verify_email(token: str, service: Annotated[UserService, Depends()]):
    return await service.check_email(token)


@user_router.post("/token", tags=["Auth"])
async def take_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()],
):
    await user_service.check_user(email=data.username, password=data.password)
    return await user_service.take_token(data.username)


@user_router.get(
    "/me",
    tags=["Profile"],
    response_model=UserProfile,
)
async def get_profile(user: current_user, service: Annotated[UserService, Depends()]):
    return await service.get_me(user.get("email"))


@user_router.put(
    "/me",
    tags=["Profile"],
    response_model=UserProfile,
    response_model_exclude_none=True,
)
async def update_profile(
    user: current_user,
    update_data: UpdateUser,
    service: Annotated[UserService, Depends()],
):
    return await service.update_profile(
        data=update_data.model_dump(), email=user.get("email")
    )


@user_router.delete("/delete-profile", tags=["Profile"])
async def delete_profile(
    user: current_user, service: Annotated[UserService, Depends()]
):
    return await service.delete_user(user.get("user_id"))


@user_router.post("/change-password", tags=["Password"])
async def change_password(
    user: current_user,
    password_data: ChangePasswordScheme,
    service: Annotated[UserService, Depends()],
):
    return await service.change_password(password_data, user.get("email"))


@user_router.post("/forgot-password", tags=["Password"])
async def forgot_password(
    service: Annotated[UserService, Depends()], email: EmailStr = Query()
):
    return await service.forgot_password(email)


@user_router.post("/set-password-via-code", tags=["Password"])
async def set_password(
    data: ChangePasswordWithCode, service: Annotated[UserService, Depends()]
):
    return await service.set_password_with_code(data)
