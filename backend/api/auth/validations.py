import secrets
from typing import Optional

from jwt.exceptions import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status, Response, Request
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer)
from pydantic import EmailStr

from backend.config import NAME_COOKIE_AUTH
from backend.api.auth import convert_jwt as auth_utils
from backend.api.auth.email_utils import send_confirm_email
from backend.api.models.models import User
from backend.api.users.db_func import get_user_by_value, create_user, update_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
http_bearer = HTTPBearer(auto_error=False)


async def get_current_auth_user(request: Request):
    session_id = request.cookies.get(NAME_COOKIE_AUTH)
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user unauthorized')
    user = await get_user_by_value(session_id, 'session_id')
    return user


async def get_current_active_auth_user(
        user: User = Depends(get_current_auth_user)
):
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not active")
    elif not user.is_confirm_to_support:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is confirm to support")
    return user


async def get_current_active_auth_user_no_raise() -> User | None:
    try:
        user = await get_current_active_auth_user()
        return user
    except:
        return


async def validate_register_auth_user(
        username: str = Form(default="Mixx"),
        email: EmailStr = Form(),
        password: str = Form(),
):
    password = auth_utils.hash_password(password)
    user = await get_user_by_value(email, is_verified=False)
    if user:
        if user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User authorized')
            # return await validate_auth_user(email=email, password=password)
    else:
        user = await create_user(username=username, email=email, password=password)
    await send_confirm_email(user.email, user.username)
    return user


async def validate_auth_user(
        email: EmailStr = Form(),
        password: str = Form(),
):
    unauth_exc = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail="invalid username or password")
    user = await get_user_by_value(email)
    if not user:
        raise unauth_exc
    if user.password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user auth in system")
    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauth_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not active")
    session_id = secrets.token_urlsafe(32)
    user = await update_user(user.email, session_id=session_id)
    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token error'
        )
    return payload
