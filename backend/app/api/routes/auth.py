from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from typing import Annotated
from fastapi import HTTPException, Depends

from fastapi import APIRouter

from app.models.user import User
from app.db.db import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, get_current_user, validate_refresh_token
from app.schemas.token_schema import Token, RefreshRequest

router = APIRouter(tags=["Token"])
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/access_token")
def login(session: T_Session, form_data: T_OAuth2PasswordRequestForm):
    user = session.scalar(select(User).where(User.username == form_data.username))
    if not user or not verify_password(form_data.password, str(user.password)):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_access_token(data={"sub": user.username, "scope": "refresh_token"})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.post("/refresh_token", response_model=Token)
def refresh_access_token(body: RefreshRequest):
    username = validate_refresh_token(body.refresh_token)
    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="Bearer")
