from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.security import get_password_hash
from app.db.db import get_session
from app.main import app
from app.models.user import table_registry
from sqlalchemy.pool import StaticPool
from app.models.user import User

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = "testpassword"
    user = User(username="testusername", email="testemail@test.com", password=get_password_hash(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user


@pytest.fixture(scope="session")
def db_url():
    return "sqlite:///./test.db"


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/token",
        data={"username": user.username, "password": user.clean_password},
    )
    return response.json()["access_token"]