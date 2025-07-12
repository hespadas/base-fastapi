from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated

from sqlalchemy import select

from app.core.security.dependencies import get_current_user
from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience_schema import ExperiencePublicSchema, ExperienceSchema
from app.db.db import get_session
from sqlalchemy.orm import Session


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


@router.get("/experiences", response_model=list[ExperiencePublicSchema])
def get_experiences(session: T_Session, current_user: T_CurrentUser):
    experiences = session.query(Experience).filter(Experience.user_id == current_user.id).all()
    return [ExperiencePublicSchema.model_validate(exp).model_dump(mode="json") for exp in experiences]


@router.get("/experiences/{experience_id}", response_model=ExperiencePublicSchema)
def get_experience_detail(experience_id: int, session: T_Session, current_user: T_CurrentUser):
    experience = session.scalar(select(Experience).where(Experience.id == experience_id))
    if not experience:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Experience not found")
    if experience.user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only view your own experiences")
    return ExperiencePublicSchema.model_validate(experience).model_dump(mode="json")


@router.put("/experiences/{experience_id}", response_model=ExperiencePublicSchema)
def update_experience(
    experience_id: int, experience: ExperienceSchema, session: T_Session, current_user: T_CurrentUser
):
    db_experience = session.scalar(select(Experience).where(Experience.id == experience_id))
    if not db_experience:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Experience not found")
    if db_experience.user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only update your own experiences")

    db_experience.title = experience.title
    db_experience.description = experience.description or ""
    db_experience.start_date = experience.start_date
    db_experience.company = experience.company
    db_experience.end_date = experience.end_date if experience.end_date else None

    session.commit()
    session.refresh(db_experience)
    return db_experience


@router.delete("/experiences/{experience_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_experience(experience_id: int, session: T_Session, current_user: T_CurrentUser):
    experience = session.scalar(select(Experience).where(Experience.id == experience_id))
    if not experience:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Experience not found")
    if experience.user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only delete your own experiences")
    session.delete(experience)
    session.commit()
    return
