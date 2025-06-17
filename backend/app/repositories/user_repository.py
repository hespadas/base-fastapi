from fastapi import Depends
from fastapi import APIRouter
from typing import Annotated

from sqlalchemy import select

from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.db.db import get_session
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, get_current_user

router = APIRouter(tags=["Users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


class UserRepository:
    def __init__(self, session: T_Session):
        self.session = session

    def create(self, user: UserSchema) -> User:
        db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_by_username_or_email(self, username: str = None, email: str = None) -> str | None:
        db_user = self.session.scalar(select(User).where((User.username == username) | (User.email == email)))
        if db_user:
            if db_user.username == username:
                return "User with this username already exists."
            if db_user.email == email:
                return "User with this email already exists."
        return None
