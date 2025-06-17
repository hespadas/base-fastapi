from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated

from app.models.user import User
from app.schemas.user_schema import UserSchema, UserPublicSchema, UserListSchema
from app.db.db import get_session
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["Users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/signup", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user_endpoint(user: UserSchema, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    detail_for_raise_if_user_exist = user_repo.get_detail_if_username_or_email_exists(
        username=user.username, email=str(user.email)
    )
    if detail_for_raise_if_user_exist:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=detail_for_raise_if_user_exist)
    created_user = user_repo.create(user)
    return created_user


@router.get("/users", response_model=UserListSchema)
def get_all_users_endpoint(session: T_Session, limit: int = 2):
    user_repo = UserRepository(session)
    users = user_repo.get_all(limit=limit)
    return {"users": users}


@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user_endpoint(user_id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser):
    user_repo = UserRepository(session)
    if user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed to update this user.")
    detail_for_raise_if_user_exist = user_repo.get_detail_if_username_or_email_exists(
        username=user.username, email=str(user.email)
    )
    if detail_for_raise_if_user_exist:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=detail_for_raise_if_user_exist)
    updated_user = user_repo.update(user_id, user)
    return updated_user


@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user_endpoint(user_id: int, session: T_Session, current_user: T_CurrentUser):
    user_repo = UserRepository(session)
    if user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed to delete this user.")
    user_repo.delete(user_id)
    return None
