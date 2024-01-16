from fastapi import FastAPI
from sqladmin import Admin

from infrastructure.main import async_engine
from presentation.endpoints.admin.users import admin_router
from presentation.endpoints.categories import category_router
from presentation.endpoints.movies import movie_router
from presentation.endpoints.users import user_router
from fastapi.middleware.cors import CORSMiddleware
from .sqladmin import MovieAdmin, UserAdmin

app = FastAPI()

admin = Admin(app, async_engine)


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin.add_view(UserAdmin)
admin.add_view(MovieAdmin)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(movie_router)
