from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import Settings

engine = create_engine(Settings().DATABASE_URL, echo=True, future=True)

def get_session() -> Session:
    with Session(engine) as session:
        yield session