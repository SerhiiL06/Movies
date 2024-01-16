from datetime import date, datetime
from typing import Annotated, Any, Optional

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr
from pydantic.functional_validators import AfterValidator

from ..movie.movie_schemes import ReadMovieScheme
from .password_schemes import validate_password

pws_validator = Annotated[str, AfterValidator(validate_password)]


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password1: pws_validator
    password2: pws_validator


class UpdateUser(BaseModel):
    birthday: Optional[date] = None
    photo: Optional[str] = None


class AdminUserScheme(BaseModel):
    id: UUID4
    email: str
    is_active: bool
    created: datetime
    role: str
    birthday: Optional[date] = None
    photo: Optional[str] = None
    movies: list[ReadMovieScheme] = None


class UserProfile(UpdateUser):
    model_config = ConfigDict(from_attributes=True)
    email: str


class UserFilterSchema(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
