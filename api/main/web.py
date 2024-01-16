from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqladmin import Admin

from infrastructure.main import async_engine
from presentation.endpoints.admin.users import admin_router
from presentation.endpoints.categories import category_router
from presentation.endpoints.movies import movie_router
from presentation.endpoints.users import user_router
from service.exceptions import (ObjectDoesntExists, PermissionDenied,
                                SomethingWentWrong)

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


@app.exception_handler(ObjectDoesntExists)
async def object_doesnt_exists_handler(request: Request, exc: ObjectDoesntExists):
    return JSONResponse(
        content={"code": "404", "msg": f"{exc.model.__name__} error"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(SomethingWentWrong)
async def something_wrong_handler(request: Request, exc: SomethingWentWrong):
    return JSONResponse(
        content={"detail": {"code": "400", "msg": "something went wrong"}},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(PermissionDenied)
async def permission_handler(request: Request, exc: PermissionDenied):
    return JSONResponse(content={"detail": {"code": "403", "msg": "Permission denied"}})
