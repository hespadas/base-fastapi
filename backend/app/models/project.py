from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import mapper_registry as registry

@registry.mapped_as_dataclass
class Project:
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    github_url: Mapped[str | None] = mapped_column(default=None)
    project_url: Mapped[str | None] = mapped_column(default=None)

