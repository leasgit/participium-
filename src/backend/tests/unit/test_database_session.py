from __future__ import annotations

import pytest

import participium.database.session as db_session


@pytest.mark.unit
def test_database_url_from_env_requires_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL environment variable is required"):
        db_session._database_url_from_env()


@pytest.mark.unit
def test_database_url_from_env_returns_configured_value(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    assert db_session._database_url_from_env() == "sqlite+pysqlite:///:memory:"


@pytest.mark.unit
def test_create_all_requires_open_connection():
    db_session.close_connection()

    with pytest.raises(RuntimeError, match="Database connection is not open"):
        db_session.create_all()


@pytest.mark.unit
def test_open_connection_configures_connection_and_get_session(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    connection = db_session.open_connection()

    try:
        assert connection is not None
        assert db_session._connection is connection

        session = db_session.get_session()
        assert session.bind is connection
    finally:
        db_session.close_connection()


@pytest.mark.unit
def test_configure_database_delegates_to_open_connection(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    connection = db_session.configure_database()

    try:
        assert connection is db_session._connection
    finally:
        db_session.close_connection()


@pytest.mark.unit
def test_close_connection_clears_global_connection(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    db_session.open_connection()
    db_session.close_connection()

    assert db_session._connection is None