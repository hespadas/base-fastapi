from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    from app.core.settings import Settings

    return create_engine(Settings().DATABASE_URL, echo=True, future=True)


def get_session():
    engine = get_engine()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with session_local() as session:
        yield session
