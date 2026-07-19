import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.api.deps as deps


def test_test_database_connection(db_session: Session) -> None:
    result = db_session.execute(text("SELECT 1")).scalar_one()

    assert result == 1


def test_get_db_closes_session(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummySession:
        closed = False

        def close(self) -> None:
            self.closed = True

    dummy_session = DummySession()
    monkeypatch.setattr(deps, "SessionLocal", lambda: dummy_session)

    dependency = deps.get_db()

    assert next(dependency) is dummy_session

    with pytest.raises(StopIteration):
        next(dependency)

    assert dummy_session.closed is True


def test_db_client_uses_overridden_session(
    db_client: TestClient,
    db_session: Session,
) -> None:
    response = db_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_db_session_fixture_has_session_type(db_session: Session) -> None:
    assert isinstance(db_session, Session)
