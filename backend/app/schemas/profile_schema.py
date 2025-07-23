from pydantic import BaseModel
from typing import List

from app.schemas.experience_schema import ExperiencePublicSchema
from app.schemas.project_schema import ProjectPublicSchema


class ProfilePublicSchema(BaseModel):
    experiences: List[ExperiencePublicSchema]
    projects: List[ProjectPublicSchema]

