from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import decode, encode, ExpiredSignatureError
from jwt.exceptions import PyJWTError
from fastapi import HTTPException
from http import HTTPStatus

from app.core import settings

settings = settings.Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
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
