from fastapi import APIRouter, Depends
from typing import Annotated

from service.users.user_service import UserService

from service.users.auth import current_user

from ..schemes.users.user_schemes import UserCreate, UserProfile, UpdateUser
from ..schemes.users.password_schemes import ChangePasswordScheme
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
async def forgot_password():
    pass
