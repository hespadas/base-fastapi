from http import HTTPStatus
from fastapi import APIRouter

from fastapi import FastAPI
from app.schemas.user_schema import UserSchema
from app.api import user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/users", status_code=HTTPStatus.CREATED, response_model=UserSchema)
def create_user():
    return 'teste'

