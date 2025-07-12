from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from typing import Annotated

from sqlalchemy import select

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


@router.put("/projects/{project_id}", response_model=ProjectPublicSchema)
def update_project(project_id: int, project: ProjectSchema, session: T_Session, current_user: T_CurrentUser):
    db_project = session.scalar(select(Project).where(Project.id == project_id))
    if not db_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Project not found")
    if db_project.user_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You can only update your own projects")

    db_project.title = project.title
    db_project.description = project.description or ""
    db_project.github_url = project.github_url
    db_project.project_url = project.project_url

    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("/projects", response_model=list[ProjectPublicSchema])
def get_projects(session: T_Session, current_user: T_CurrentUser):
    if not current_user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Not authenticated")
    projects = session.scalars(select(Project).where(Project.user_id == current_user.id)).all()
    return projects


