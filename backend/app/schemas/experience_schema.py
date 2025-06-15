from pydantic import BaseModel
from datetime import datetime


class ExperienceSchema(BaseModel):
    title: str
    company: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    description: str | None = None
    user_id: int | None = None


class ExperiencePublicSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    company: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
