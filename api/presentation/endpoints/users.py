from fastapi import APIRouter
from service.users.user_service import UserService
from ..schemes.users.user_schemes import UserCreate
from fastapi import Depends


user_router = APIRouter()


@user_router.post("/register", tags=["Auth"])
async def register(user_data: UserCreate, service: UserService = Depends()):
    res = await service.register_user(
        username=user_data.username,
        email=user_data.email,
        password1=user_data.password1,
        password2=user_data.password2,
    )
    return res


@user_router.post("/login", tags=["Auth"])
async def login():
    pass


@user_router.post("/token", tags=["Auth"])
async def token():
    pass


@user_router.get("/me", tags=["Profile"])
async def get_profile():
    pass


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
