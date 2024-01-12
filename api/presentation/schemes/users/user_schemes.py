from typing import Any, Optional
from typing import Annotated
from datetime import date
import re
from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from pydantic.functional_validators import AfterValidator
from .password_schemes import validate_password


pws_validator = Annotated[str, AfterValidator(validate_password)]


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    password1: pws_validator
    password2: pws_validator

    # @field_validator("username")
    # @classmethod
    # def validate_unique(cls, value):
    #     return value.lower()

    # @field_validator("password1", "password2")
    # @staticmethod
    # def validate_password(cls, value):
    #     PasswordValidator(value)
    #     return value

    # @field_validator("password1", "password2")
    # @staticmethod
    # def _validate(value):
    #     if len(value) < 5:
    #         raise ValueError("Password must have 5 elements minimum")

    #     if len(value) > 40:
    #         raise ValueError("Password is too long")

    #     if not re.fullmatch(r"[A-Za-z0-9]+", value):
    #         raise ValueError("Password cannot have special symbols")

    #     return value


class UpdateUser(BaseModel):
    username: str
    birthday: Optional[date] = None
    photo: Optional[str] = None


class UserProfile(UpdateUser):
    model_config = ConfigDict(from_attributes=True)
    email: str
