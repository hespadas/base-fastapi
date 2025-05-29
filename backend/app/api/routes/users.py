from http import HTTPStatus
from fastapi import HTTPException, Depends

from fastapi import APIRouter

from app.models.user import User
from app.schemas.user_schema import UserSchema, UserPublicSchema, UserListSchema
from app.db.db import get_session
from sqlalchemy import select

router = APIRouter(tags=["Users"])


@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
            select(User).where((User.username == user.username) | (User.email == user.email))
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User with this username already exists."
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User with this email already exists."
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users", response_model=UserListSchema)
def get_users(
        limit: int=2,
        session=Depends(get_session)
     ):
    user = session.scalars(select(User).limit(limit))
    return {
        "users": user
    }



@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(
        user_id: int,
        user: UserSchema,
        session=Depends(get_session)
    ):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)
    return db_user




@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(
        user_id: int,
        session=Depends(get_session)
    ):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )
    session.delete(db_user)
    session.commit()
    return None

