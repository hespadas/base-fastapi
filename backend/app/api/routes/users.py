from http import HTTPStatus
from fastapi import APIRouter

from app.schemas.user_schema import UserSchema, UserPublicSchema

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    return user


@router.get("/users", response_model=UserPublicSchema)
def get_users():
    pass

@router.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    pass

@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    pass