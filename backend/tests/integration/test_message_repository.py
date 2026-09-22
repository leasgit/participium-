from __future__ import annotations

import time
import pytest

from participium.database import close_connection, create_all, get_session, open_connection
from participium.models.category import Category
from participium.models.enums import ReportStatus, Role
from participium.models.message import Message
from participium.models.report import Report
from participium.models.user import User
from participium.repositories.message_repository import MessageRepository


@pytest.fixture
def session(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    open_connection()
    create_all()
    s = get_session()
    yield s
    close_connection()


@pytest.fixture
def seeded(session):
    category = Category(name="Roads", is_active=True)
    session.add(category)
    session.flush()

    citizen = User(
        username="citizen1", email="c1@example.com", password_hash="x",
        first_name="Alice", last_name="Smith", role=Role.CITIZEN,
    )
    operator = User(
        username="op1", email="op1@example.com", password_hash="x",
        first_name="Bob", last_name="Jones", role=Role.OPERATOR,
        category_id=category.id,
    )
    session.add_all([citizen, operator])
    session.flush()

    report_a = Report(
        title="Report A", description="Desc A", latitude=42.0, longitude=12.0,
        status=ReportStatus.ASSIGNED, reporter_id=citizen.id, category_id=category.id,
    )
    report_b = Report(
        title="Report B", description="Desc B", latitude=43.0, longitude=13.0,
        status=ReportStatus.ASSIGNED, reporter_id=citizen.id, category_id=category.id,
    )
    session.add_all([report_a, report_b])
    session.commit()

    return {
        "session": session,
        "citizen": citizen,
        "operator": operator,
        "report_a": report_a,
        "report_b": report_b,
    }


def test_add_persists_message(seeded):
    s = seeded["session"]
    repo = MessageRepository(s)

    msg = Message(
        report_id=seeded["report_a"].id,
        sender_id=seeded["operator"].id,
        recipient_id=seeded["citizen"].id,
        body="We are handling it.",
    )
    repo.add(msg)
    s.commit()

    results = repo.list_for_report(seeded["report_a"].id)
    assert len(results) == 1
    assert results[0].body == "We are handling it."


def test_add_returns_the_message(seeded):
    s = seeded["session"]
    repo = MessageRepository(s)

    msg = Message(
        report_id=seeded["report_a"].id,
        sender_id=seeded["operator"].id,
        recipient_id=seeded["citizen"].id,
        body="Hello",
    )
    assert repo.add(msg) is msg


def test_list_for_report_empty_when_no_messages(seeded):
    repo = MessageRepository(seeded["session"])
    assert repo.list_for_report(seeded["report_a"].id) == []


def test_list_for_report_scoped_to_report_id(seeded):
    s = seeded["session"]
    repo = MessageRepository(s)

    repo.add(Message(
        report_id=seeded["report_a"].id,
        sender_id=seeded["operator"].id,
        recipient_id=seeded["citizen"].id,
        body="For report A",
    ))
    repo.add(Message(
        report_id=seeded["report_b"].id,
        sender_id=seeded["operator"].id,
        recipient_id=seeded["citizen"].id,
        body="For report B",
    ))
    s.commit()

    results = repo.list_for_report(seeded["report_a"].id)
    assert len(results) == 1
    assert results[0].body == "For report A"


def test_list_for_report_ordered_oldest_first(seeded):
    s = seeded["session"]
    repo = MessageRepository(s)

    repo.add(Message(
        report_id=seeded["report_a"].id,
        sender_id=seeded["operator"].id,
        recipient_id=seeded["citizen"].id,
        body="First",
    ))
    s.commit()

    time.sleep(0.01)

    repo.add(Message(
        report_id=seeded["report_a"].id,
        sender_id=seeded["citizen"].id,
        recipient_id=seeded["operator"].id,
        body="Second",
    ))
    s.commit()

    results = repo.list_for_report(seeded["report_a"].id)
    assert results[0].body == "First"
    assert results[1].body == "Second"