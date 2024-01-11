from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from infrastructure.db import config


class JWTServive:
    def create_jwt(self, email):
        exp = datetime.now() + timedelta(hours=3)

        payload = {"email": email, "exp": exp}
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

        return token

    def decode_jwt(self, token):
        data = jwt.decode(token, config.SECRET_KEY)

        format_time = datetime.fromtimestamp(data["exp"])
        if format_time < datetime.now():
            raise HTTPException(detail="token was expired")

        return data["email"]
