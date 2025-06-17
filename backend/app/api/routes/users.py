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
from app.repositories.user_repository import UserRepository


router = APIRouter(tags=["Users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user_endpoint(user: UserSchema, session: Session = Depends(get_session)):
    repo = UserRepository(session)
    detail_for_raise_if_user_exist = repo.get_by_username_or_email(username=user.username, email=str(user.email))
    if detail_for_raise_if_user_exist:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=detail_for_raise_if_user_exist)
    created_user = repo.create(user)
    return created_user


@router.get("/users", response_model=UserListSchema)
def get_users_endpoint(session: T_Session, limit: int = 2):
    user = session.scalars(select(User).limit(limit))
    return {"users": user}


@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user_endpoint(user_id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser):
    if user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed to update this user.")
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user_endpoint(user_id: int, session: T_Session, current_user: T_CurrentUser):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if current_user.id != db_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only delete your own account.")
    session.delete(db_user)
    session.commit()
    return
