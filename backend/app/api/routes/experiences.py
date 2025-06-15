from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated
from datetime import datetime

from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience_schema import ExperiencePublicSchema, ExperienceSchema
from app.db.db import get_session
from sqlalchemy.orm import Session
from app.core.security import get_current_user


router = APIRouter(tags=["Experiences"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/experiences", status_code=HTTPStatus.CREATED, response_model=ExperiencePublicSchema)
def create_experience(experience: ExperienceSchema, session: T_Session, current_user: T_CurrentUser):
    if not current_user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Not authenticated")
    new_experience = Experience(
        title=experience.title,
        description=experience.description or "",
        start_date=experience.start_date,
        user_id=current_user.id,
        company=experience.company,
        end_date=experience.end_date if experience.end_date else None,
    )
    session.add(new_experience)
    session.commit()
    session.refresh(new_experience)
    return new_experience

@router.get("/experiences/{user_id}", response_model=dict[str, list[ExperiencePublicSchema]])
def get_experiences(user_id: int, session: T_Session):
    experiences = session.query(Experience).filter(Experience.user_id == user_id).all()
    if not experiences:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No experiences found for this user")
    return {"experiences": [ExperiencePublicSchema.model_validate(experience).model_dump(mode="json") for experience in experiences]}

