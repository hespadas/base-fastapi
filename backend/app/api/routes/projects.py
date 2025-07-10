from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated


from app.core.security.dependencies import get_current_user
from app.models.project import Project
from app.models.user import User
from app.db.db import get_session
from sqlalchemy.orm import Session

from app.schemas.project_schema import ProjectSchema, ProjectPublicSchema

router = APIRouter(tags=["Projects"])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/projects", status_code=HTTPStatus.CREATED, response_model=ProjectPublicSchema)
def create_project(project: ProjectSchema, session: T_Session, current_user: T_CurrentUser):
    if not current_user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Not authenticated")
    new_project = Project(
        title=project.title,
        description=project.description or "",
        user_id=current_user.id,
        github_url=project.github_url,
        project_url=project.project_url,
    )
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project
