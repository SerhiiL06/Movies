from fastapi import FastAPI
from presentation.endpoints.users import user_router
from presentation.endpoints.admin.main import admin_router

app = FastAPI()


app.include_router(user_router)
app.include_router(admin_router)


@app.get("/")
async def main_paig():
    return {"hello": "world"}
