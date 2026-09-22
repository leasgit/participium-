from __future__ import annotations

import pytest
from unittest.mock import Mock

from participium.core.exceptions import AuthorizationError, ValidationError
from participium.models.enums import Role
from participium.services.messaging_service import MessagingService

@pytest.fixture
def mocked_dependencies():
    """Create and return mocks for all MessagingService dependencies."""
    session = Mock()
    report_repository = Mock()
    message_repository = Mock()
    notification_service = Mock()
    return session, report_repository, message_repository, notification_service

@pytest.fixture
def messaging_service(mocked_dependencies):
    """Initialize MessagingService with mocked dependencies."""
    session, report_repository, message_repository, notification_service = mocked_dependencies
    return MessagingService(
        session=session,
        report_repository=report_repository,
        message_repository=message_repository,
        notification_service=notification_service,
    )


def make_user(user_id=1, role=Role.CITIZEN, category_id=None,
              first_name="Alice", last_name="Smith", username="alice"):
    u = Mock()
    u.id = user_id
    u.role = role
    u.category_id = category_id
    u.first_name = first_name
    u.last_name = last_name
    u.username = username
    return u


def make_report(reporter_id=1, category_id=5, reporter=None, status_history=None):
    r = Mock()
    r.id = 10
    r.reporter_id = reporter_id
    r.category_id = category_id
    r.reporter = reporter or make_user(user_id=reporter_id)
    r.status_history = status_history or []
    return r


@pytest.mark.parametrize("user, report, oracle", [
    (None, make_report(), False),  # no user
    (make_user(role=Role.ADMIN), make_report(reporter_id=99), True), # admin
    (make_user(role=Role.OPERATOR, category_id=5), make_report(category_id=5), True),   # operator same category
    (make_user(user_id=1, role=Role.CITIZEN),      make_report(reporter_id=1), True),   # reporter
    (make_user(user_id=99, role=Role.CITIZEN),     make_report(reporter_id=1), False),  # other citizen
])
def test_can_access_thread(messaging_service, user, report, oracle):
    assert messaging_service.can_access_thread(report, user) == oracle

@pytest.mark.parametrize("first, last, username, oracle", [
    ("John", "Doe", "jdoe", "John Doe"),  # full name
    ("", "", "jdoe", "jdoe"),      # fallback to username
    ("Anna", "", "anna", "Anna"),      # first name only
])
def test_sender_name(first, last, username, oracle):
    user = make_user(first_name=first, last_name=last, username=username)
    assert MessagingService._sender_name(user) == oracle


@pytest.mark.parametrize("sender, body, expected_exception", [
    (make_user(user_id=99, role=Role.CITIZEN), "hello", AuthorizationError),  # no access
    (make_user(user_id=1,  role=Role.CITIZEN), "   ",   ValidationError),     # blank body
    (make_user(user_id=1,  role=Role.CITIZEN), "",      ValidationError),     # empty body
])
def test_send_message_raises(messaging_service, mocked_dependencies, sender, body, expected_exception):
    _, _, message_repository, _ = mocked_dependencies
    message_repository.list_for_report.return_value = []
    report = make_report(reporter_id=1, status_history=[])

    with pytest.raises(expected_exception):
        messaging_service.send_message(report, sender, body)


def test_send_message_no_recipient_raises(messaging_service, mocked_dependencies):
    _, _, message_repository, _ = mocked_dependencies
    message_repository.list_for_report.return_value = []

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    report = make_report(reporter_id=1, status_history=[])

    with pytest.raises(ValidationError, match="No recipient"):
        messaging_service.send_message(report, reporter, "hello")


def test_send_message_saves_and_commits(messaging_service, mocked_dependencies):
    session, _, message_repository, _ = mocked_dependencies

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    operator = make_user(user_id=2, role=Role.OPERATOR, category_id=5)
    report = make_report(reporter_id=1, category_id=5, reporter=reporter)

    messaging_service.send_message(report, operator, "We are on it.")

    message_repository.add.assert_called_once()
    session.commit.assert_called_once()


def test_send_message_body_is_stripped(messaging_service, mocked_dependencies):
    _, _, message_repository, _ = mocked_dependencies

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    operator = make_user(user_id=2, role=Role.OPERATOR, category_id=5)
    report = make_report(reporter_id=1, category_id=5, reporter=reporter)

    messaging_service.send_message(report, operator, "  trimmed  ")

    added = message_repository.add.call_args[0][0]
    assert added.body == "trimmed"


def test_send_message_fires_notification(messaging_service, mocked_dependencies):
    _, _, _, notification_service = mocked_dependencies

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    operator = make_user(user_id=2, role=Role.OPERATOR, category_id=5)
    report = make_report(reporter_id=1, category_id=5, reporter=reporter)

    messaging_service.send_message(report, operator, "Update.")

    notification_service.notify_new_message.assert_called_once()


def test_resolve_recipient_operator_gets_reporter(messaging_service):
    reporter = make_user(user_id=1)
    operator = make_user(user_id=2, role=Role.OPERATOR, category_id=5)
    report = make_report(reporter_id=1, category_id=5, reporter=reporter)

    assert messaging_service._resolve_recipient(report, operator) is reporter


def test_resolve_recipient_admin_gets_reporter(messaging_service):
    reporter = make_user(user_id=1)
    admin = make_user(user_id=5, role=Role.ADMIN)
    report = make_report(reporter_id=1, reporter=reporter)

    assert messaging_service._resolve_recipient(report, admin) is reporter


def test_resolve_recipient_citizen_gets_operator_from_messages(messaging_service, mocked_dependencies):
    _, _, message_repository, _ = mocked_dependencies

    op_user = make_user(user_id=3, role=Role.OPERATOR)
    prior_msg = Mock()
    prior_msg.sender = op_user
    message_repository.list_for_report.return_value = [prior_msg]

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    report = make_report(reporter_id=1, reporter=reporter)

    assert messaging_service._resolve_recipient(report, reporter) is op_user


def test_resolve_recipient_citizen_falls_back_to_status_history(messaging_service, mocked_dependencies):
    _, _, message_repository, _ = mocked_dependencies
    message_repository.list_for_report.return_value = []

    op_user = make_user(user_id=7, role=Role.OPERATOR)
    status_entry = Mock()
    status_entry.changed_by = op_user

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    report = make_report(reporter_id=1, reporter=reporter, status_history=[status_entry])

    assert messaging_service._resolve_recipient(report, reporter) is op_user


def test_resolve_recipient_returns_none_when_no_operator_found(messaging_service, mocked_dependencies):
    _, _, message_repository, _ = mocked_dependencies
    message_repository.list_for_report.return_value = []

    reporter = make_user(user_id=1, role=Role.CITIZEN)
    report = make_report(reporter_id=1, status_history=[])

    assert messaging_service._resolve_recipient(report, reporter) is None