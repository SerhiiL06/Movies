from datetime import date
from typing import Annotated, Any, Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.functional_validators import AfterValidator

from .password_schemes import validate_password

pws_validator = Annotated[str, AfterValidator(validate_password)]


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    password1: pws_validator
    password2: pws_validator


class UpdateUser(BaseModel):
    username: str
    birthday: Optional[date] = None
    photo: Optional[str] = None


class UserProfile(UpdateUser):
    model_config = ConfigDict(from_attributes=True)
    email: str
