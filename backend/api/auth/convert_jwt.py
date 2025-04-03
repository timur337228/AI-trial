import jwt
import bcrypt
from datetime import timedelta, datetime
from backend.config import settings


def hash_password(
        password: str
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password
    )
