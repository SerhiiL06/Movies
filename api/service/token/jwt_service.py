from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from infrastructure.db import config


class JWTServive:
    async def create_access_token(self, data):
        exp = datetime.now() + timedelta(minutes=20)

        payload = {
            "user_id": str(data.id),
            "email": data.email,
            "role": data.role,
            "exp": exp,
        }

        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}

    def create_jwt(self, email):
        exp = datetime.now() + timedelta(hours=3)

        payload = {"email": email, "exp": exp}
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

        return token

    def decode_jwt(self, token):
        data = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=["HS256"])

        format_time = datetime.fromtimestamp(data["exp"])
        if format_time < datetime.now():
            raise HTTPException(detail="token was expired")

        return data
