import os
from collections.abc import Generator

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from alembic import command
from app.core import config as config_module
from app.core.config import Settings

TEST_DATABASE_URL = Settings().test_database_url


def _assert_safe_test_database_url(database_url: str) -> None:
    url = make_url(database_url)
    database_name = url.database or ""

    if "test" not in database_name.lower():
        raise RuntimeError("TEST_DATABASE_URL must point to a database whose name contains 'test'.")

    if database_url == Settings().database_url:
        raise RuntimeError("TEST_DATABASE_URL must not be the same as DATABASE_URL.")


_assert_safe_test_database_url(TEST_DATABASE_URL)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
config_module.get_settings.cache_clear()
config_module.settings = config_module.get_settings()

from app.api.deps import get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def test_database_url() -> str:
    return TEST_DATABASE_URL


@pytest.fixture(scope="session")
def test_engine(test_database_url: str) -> Generator[Engine, None, None]:
    engine = create_engine(test_database_url, pool_pre_ping=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    return Config("alembic.ini")


@pytest.fixture
def migrated_database(alembic_config: Config) -> Generator[None, None, None]:
    command.upgrade(alembic_config, "head")
    yield


@pytest.fixture
def db_session(
    migrated_database: None,
    test_engine: Engine,
) -> Generator[Session, None, None]:
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        with test_engine.begin() as connection:
            connection.execute(text("TRUNCATE TABLE users CASCADE"))


@pytest.fixture
def db_client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
