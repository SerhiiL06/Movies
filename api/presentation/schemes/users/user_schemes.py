from typing import Any, Optional
from datetime import date
from dataclasses import dataclass
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
            raise ValueError(f"{value} is too short")

        return value


class UpdateUser(BaseModel):
    username: str
    birthday: Optional[date] = None
    photo: Optional[str] = None


class UserProfile(UpdateUser):
    model_config = ConfigDict(from_attributes=True)
    email: str
