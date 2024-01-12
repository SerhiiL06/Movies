from datetime import datetime, timedelta
from infrastructure.main import async_session
from fastapi import HTTPException
from jose import jwt

from infrastructure.db import config


class JWTServive:
    def auth(self, email):
        exp = datetime.now() + timedelta(minutes=20)

        payload = {"email": email, "exp": exp}

        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
        print(token)
        return {"access_token": token, "token_type": "bearer"}

    def create_jwt(self, email):
        exp = datetime.now() + timedelta(hours=3)

        payload = {"email": email, "exp": exp}
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

        return token

    def decode_jwt(self, token):
        data = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=["HS256"])

        # format_time = datetime.fromtimestamp(data["exp"])
        # if format_time < datetime.now():
        #     raise HTTPException(detail="token was expired")

        return data
