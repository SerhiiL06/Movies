from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, validate_email


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str
    password1: str
    password2: str

    @field_validator("email", "username")
    @classmethod
    def validate_email(cls, value):
        return value.upper()

    @field_validator("password1", "password2")
    @classmethod
    def validate_email(cls, value):
        if len(value) < 5:
            raise ValueError(f"{value} is to short")

        return value
