import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User


def test_create_and_query_user(db_session: Session) -> None:
    user = User(
        username="alice",
        email="alice@example.com",
        password_hash="not-a-real-hash-yet",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = db_session.get(User, user.id)

    assert saved_user is not None
    assert isinstance(saved_user.id, uuid.UUID)
    assert saved_user.username == "alice"
    assert saved_user.email == "alice@example.com"
    assert saved_user.display_name is None
    assert saved_user.is_active is True
    assert saved_user.is_superuser is False
    assert saved_user.created_at.tzinfo is not None
    assert saved_user.updated_at.tzinfo is not None


def test_display_name_can_be_none(db_session: Session) -> None:
    user = User(
        username="bob",
        email="bob@example.com",
        display_name=None,
        password_hash="not-a-real-hash-yet",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.display_name is None


def test_username_must_be_unique(db_session: Session) -> None:
    db_session.add_all(
        [
            User(
                username="duplicate-name",
                email="first@example.com",
                password_hash="not-a-real-hash-yet",
            ),
            User(
                username="duplicate-name",
                email="second@example.com",
                password_hash="not-a-real-hash-yet",
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_email_must_be_unique(db_session: Session) -> None:
    db_session.add_all(
        [
            User(
                username="charlie",
                email="duplicate@example.com",
                password_hash="not-a-real-hash-yet",
            ),
            User(
                username="diana",
                email="duplicate@example.com",
                password_hash="not-a-real-hash-yet",
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
