from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
    from app.core.settings import Settings
    return create_engine(Settings().DATABASE_URL, echo=True, future=True)

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as session:
        yield session
