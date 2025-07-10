from pydantic import BaseModel, ConfigDict

class ProjectSchema(BaseModel):
    title: str
    user_id: int
    description: str | None = None
    github_url: str | None = None
    project_url: str | None = None


class ProjectPublicSchema(BaseModel):
    id: int
    title: str
    user_id: int
    description: str | None = None
    github_url: str | None = None
    project_url: str | None = None
    model_config = ConfigDict(from_attributes=True)
