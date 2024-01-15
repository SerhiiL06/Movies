from sqladmin import Admin, ModelView, fields
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from wtforms import BooleanField, EmailField, Form, SelectField

from infrastructure.db.models.movie import Movie
from infrastructure.db.models.user import User
from service.users.user_service import UserService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        auth = UserService()
        form = await request.form()
        username, password = form["username"], form["password"]
        auth.check_user(username, password)
        token = auth.take_token(username)
        # Validate username/password credentials
        # And update session
        request.session.update({"token": token.get("access_token")})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


class CreateFormUser(Form):
    email = EmailField()
    role = SelectField(choices=["admin", "default"])
    is_active = BooleanField(default=False)
    birthday = fields.DateField()


class UserAdmin(ModelView, model=User):
    form = CreateFormUser
    column_list = [User.email, User.is_active, User.created]
    column_details_list = [
        User.email,
        User.birthday,
        User.photo,
        User.created,
        User.movies,
    ]
    column_formatters = {
        User.created: lambda x, a: x.created.date(),
    }
    column_searchable_list = [User.email]
    column_sortable_list = [User.email]


class MovieAdmin(ModelView, model=Movie):
    column_list = [Movie.title, Movie.description]
