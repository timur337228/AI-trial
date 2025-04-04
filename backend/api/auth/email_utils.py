import secrets

import aiosmtplib
from jinja2 import Environment, FileSystemLoader
from itsdangerous import URLSafeTimedSerializer
from fastapi import HTTPException, status

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pydantic import EmailStr

from backend.config import settings, BASE_DIR
from backend.api.users.db_func import update_user, get_user_by_value

SECRET_KEY = settings.AUTH_JWT.private_key_path.read_text()
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_email_confirmation_token(email: EmailStr):
    return serializer.dumps(email.lower(), salt=settings.EMAIL_SALT)


async def confirm_email_confirmation_token(token):
    try:
        error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid token")
        email = serializer.loads(token, salt=settings.EMAIL_SALT)
        if not email:
            raise error
        user = await get_user_by_value(email, is_verified=False)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный или просроченный токен")
        if user.token_verified != token:
            raise error
        session_id = secrets.token_urlsafe(32)
        user = await update_user(user.email, is_verified=True, token_verified=None, session_id=session_id)
        return user
    except:
        return


async def send_email(sender_email: EmailStr,
                     receiver_email: str,
                     password: str,
                     subject: str,
                     body: str,
                     smtp_server: str = "smtp.gmail.com",
                     smtp_port: int = 587):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    try:
        async with aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port) as smtp:
            await smtp.login(sender_email, password)
            await smtp.send_message(message)
            return True
    except Exception:
        return


async def send_confirm_email(email: EmailStr, name: str):
    sender_email = settings.EMAIL
    subject = "Подтверждение почты"
    env = Environment(loader=FileSystemLoader(f"{BASE_DIR}/api/templates"))
    template = env.get_template("mail.html")
    token = generate_email_confirmation_token(email)
    confirmation_url = f"{settings.BASE_URL}/confirm_email/?token={token}"
    await update_user(email, token_verified=token)
    body = template.render(username=name,
                           confirmation_url=confirmation_url)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    password = settings.SMTP
    try:
        await send_email(sender_email, email, password, subject, body, smtp_server, smtp_port)
    except:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid email or password")
