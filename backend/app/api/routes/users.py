from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated

from app.models.user import User
from app.schemas.user_schema import UserSchema, UserPublicSchema, UserListSchema
from app.db.db import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, get_current_user

router = APIRouter(tags=["Users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User with this username already exists.")
        if db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User with this email already exists.")
    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users", response_model=UserListSchema)
def get_users(session: T_Session, limit: int = 2):
    user = session.scalars(select(User).limit(limit))
    return {"users": user}


@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser):
    if user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only update your own account.")
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if current_user.id != db_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only delete your own account.")
    session.delete(db_user)
    session.commit()
    return


