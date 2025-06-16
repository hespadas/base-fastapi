from pydantic import BaseModel, ConfigDict
from datetime import date


class ExperienceSchema(BaseModel):
    title: str
    company: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    user_id: int | None = None


class ExperiencePublicSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    company: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    model_config = ConfigDict(from_attributes=True)
