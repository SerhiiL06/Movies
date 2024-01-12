from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
import re
from typing import Annotated


def validate_password(value):
    if len(value) < 5:
        raise ValueError("Password must have 5 elements minimum")

    if len(value) > 40:
        raise ValueError("Password is too long")

    if not re.fullmatch(r"[A-Za-z0-9]+", value):
        raise ValueError("Password cannot have special symbols")

    return value


pws_validator = Annotated[str, AfterValidator(validate_password)]


class ChangePasswordScheme(BaseModel):
    password1: str
    password2: str

    new_password: pws_validator
