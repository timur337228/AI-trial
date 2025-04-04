import secrets

from fastapi import APIRouter, Depends, Header, status, Path, Query, Request, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

from backend.config import settings, NAME_COOKIE_AUTH, BASE_PARAM_COOKIE
from backend.api.users.db_func import update_user, get_user_by_value, create_user
from backend.api.auth.validations import (
    validate_auth_user,
    validate_register_auth_user,
)
from backend.api.auth.validations import http_bearer, get_current_active_auth_user, get_current_auth_user

from backend.api.auth.email_utils import confirm_email_confirmation_token
from backend.api.models.models import User


prefix = "/auth"

router = APIRouter(prefix=prefix, tags=['auth'])


@router.post('/register/')
async def register_auth_user_jwt(
        user: User = Depends(validate_register_auth_user)
):
    return {"message": 'Good reg, confirm email'}


@router.post('/login/')
async def auth_user_jwt(
        response: Response,
        user: User = Depends(validate_auth_user)
):
    response.set_cookie(
        key=NAME_COOKIE_AUTH,
        value=user.session_id,
        **BASE_PARAM_COOKIE
    )
    return {"status": "success"}


@router.get("/user/me/", )
async def auth_user_check_self_info(
        user: User = Depends(get_current_active_auth_user)
):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


@router.post("/confirm-email/")
async def confirm_email(response: Response,
                        token: str = Query()):
    user = await confirm_email_confirmation_token(token)
    response.set_cookie(
        key=NAME_COOKIE_AUTH,
        value=user.session_id,
        **BASE_PARAM_COOKIE
    )
    return {'message': 'Good confirm Email'}


@router.get("/logout/")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        await update_user(session_id, 'session_id', session_id=None)

    response = JSONResponse(
        content={"message": "Logout successful"})
    response.delete_cookie(NAME_COOKIE_AUTH)
    return response