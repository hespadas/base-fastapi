from http import HTTPStatus
from fastapi import HTTPException

from fastapi import APIRouter

from app.core.settings import Settings
from app.models.user import User
from app.schemas.user_schema import UserSchema, UserPublicSchema
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)
    with Session(engine) as session:
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


@router.get("/users", response_model=UserPublicSchema)
def get_users():
    pass


@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    pass


@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    pass
