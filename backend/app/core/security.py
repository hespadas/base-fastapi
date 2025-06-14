from http import HTTPStatus
from zoneinfo import ZoneInfo

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from pwdlib import PasswordHash
from jwt import decode, encode, ExpiredSignatureError
from jwt.exceptions import PyJWTError
from sqlalchemy import select

from app.core import settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.db import get_session
from app.models.user import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

settings = settings.Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_refresh_token(refresh_token: str) -> str:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "refresh_token":
            raise credentials_exception
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        return username
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWTError:
        raise credentials_exception


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
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
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = session.scalar(select(User).where(User.username == username))
    if not user:
        raise credentials_exception
    return user

