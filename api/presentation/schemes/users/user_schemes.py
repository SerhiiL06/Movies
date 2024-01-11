from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator, EmailStr


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    password1: str
    password2: str

    @field_validator("username")
    @classmethod
    def validate_unique(cls, value):
        return value.lower()

    @field_validator("password1", "password2")
    @classmethod
    def validate_email(cls, value):
        if len(value) < 5:
            raise ValueError(f"{value} is to short")

        return value
