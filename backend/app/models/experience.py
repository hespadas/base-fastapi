from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import mapper_registry as registry


@registry.mapped_as_dataclass
class Experience:
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[date] = mapped_column(default=None)
    end_date: Mapped[date | None] = mapped_column(default=None)
    company: Mapped[str | None] = mapped_column(default=None)
