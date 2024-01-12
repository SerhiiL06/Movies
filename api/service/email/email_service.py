from fastapi_mail import FastMail, MessageSchema

from infrastructure.db.config import email_settings
from service.token.jwt_service import JWTServive


class EmailService:
    def __init__(self):
        self.mail = FastMail(config=email_settings.get_email_config)
        self.jwt = JWTServive()

    async def send_email_verification(self, email: str):
        token = self.jwt.create_jwt(email)
        link = f"http://127.0.0.1:8000/users/email-verification/{token}"
        body = f"""<p>Hello sir! Click here for verify your email {link}</p>"""

        message = MessageSchema(
            recipients=[email],
            subject="Your email verification link",
            body=body,
            subtype="html",
        )

        await self.mail.send_message(message)
