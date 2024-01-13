from fastapi import FastAPI
from redis import asyncio as aioredis

from presentation.endpoints.admin.main import admin_router
from presentation.endpoints.users import user_router
from presentation.endpoints.categories import category_router

app = FastAPI()


app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
