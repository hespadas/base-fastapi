from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated

from sqlalchemy import select
#
from app.core.security.dependencies import get_current_user
from app.models.experience import Experience
from app.models.project import Project
# from app.models.profile import Profile
from app.models.user import User
# from app.schemas.profile_schema import ProfilePublicSchema, ProfileSchema
from app.db.db import get_session
from sqlalchemy.orm import Session

from app.schemas.experience_schema import ExperiencePublicSchema
from app.schemas.profile_schema import ProfilePublicSchema
from app.schemas.project_schema import ProjectPublicSchema

router = APIRouter(tags=["Experiences"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/profile/{user_id}", response_model=ProfilePublicSchema)
def get_profile(user_id: int, session: T_Session):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    experiences = session.scalars(select(Experience).where(Experience.user_id == user_id)).all()
    projects = session.scalars(select(Project).where(Project.user_id == user_id)).all()

    return {
        "experiences": [ExperiencePublicSchema.model_validate(exp).model_dump(mode="json") for exp in experiences],
        "projects": [ProjectPublicSchema.model_validate(proj).model_dump(mode="json") for proj in projects]
    }