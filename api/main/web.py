from fastapi import FastAPI
from sqladmin import Admin

from infrastructure.main import async_engine
from presentation.endpoints.admin.main import admin_router
from presentation.endpoints.categories import category_router
from presentation.endpoints.movies import movie_router
from presentation.endpoints.users import user_router

from .sqladmin import MovieAdmin, UserAdmin

app = FastAPI()

admin = Admin(app, async_engine)


admin.add_view(UserAdmin)
admin.add_view(MovieAdmin)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(movie_router)
