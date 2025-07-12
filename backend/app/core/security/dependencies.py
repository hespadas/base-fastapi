from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from http import HTTPStatus
from jwt import decode, ExpiredSignatureError
from jwt.exceptions import PyJWTError

from app.db.db import get_session
from app.models.user import User
from app.core import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/access_token")
settings = settings.Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except (ExpiredSignatureError, PyJWTError):
        raise credentials_exception
    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise credentials_exception
    return user
