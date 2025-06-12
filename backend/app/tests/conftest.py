from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
import factory
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.db import get_session
from app.main import app
from app.models.user import table_registry
from sqlalchemy.pool import StaticPool
from app.models.user import User
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:latest") as postgres:
        _engine = create_engine(
            postgres.get_connection_url(),
        )
        with _engine.begin():
            yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        return session
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()
    table_registry.metadata.drop_all(engine)


@pytest_asyncio.fixture
async def user(session):
    pwd = "testpassword"
    user = UserFactory(password=get_password_hash(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user


@pytest_asyncio.fixture
async def another_user(session):
    another_user = UserFactory()
    session.add(another_user)
    session.commit()
    session.refresh(another_user)
    return another_user


@pytest.fixture(scope="session")
def db_url():
    return "sqlite:///./test.db"


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/access_token",
        data={"username": user.username, "password": user.clean_password},
    )
    return response.json()["access_token"]


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
