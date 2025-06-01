from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from fastapi import HTTPException, Depends

from fastapi import APIRouter

from app.models.user import User
from app.db.db import get_session
from sqlalchemy import select
from app.core.security import verify_password

router = APIRouter(tags=["Token"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm =Depends(),
          session=Depends(get_session)):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
        )
