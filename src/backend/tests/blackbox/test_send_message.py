from __future__ import annotations

import pytest

from backend.participium.core.exceptions import AuthorizationError, ValidationError
from backend.participium.models.enums import ReportStatus
from participium.services.messaging_service import MessagingService
from participium.models.user import User
from participium.models.report import Report



AUTHORIZED_USER = User(
    id=101,
    username="maria.rossi",
    first_name="Maria",
    last_name="Rossi",
    email="maria.rossi@example.com",
    password_hash="HASHED_PASSWORD_101",
    is_active=True,
    is_email_verified=True,
)

UNAUTHORIZED_USER = User(
    id=102,
    username="mario.verdi",
    first_name="Mario",
    last_name="Verdi",
    email="mario.verdi@example.com",
    password_hash="HASHED_PASSWORD_102",
    is_active=True,
    is_email_verified=True,
)

REPORT_WITH_RECIPIENT = Report(
    id=100,
    title="Report100",
    description="Description",
    latitude=10.0,
    longitude=10.0,
    is_anonymous=False,
    status=ReportStatus.IN_PROGRESS,
    reporter_id=101,
    reporter=AUTHORIZED_USER,
)

REPORT_WITHOUT_RECIPIENT = Report(
    id=101,
    title="Report101",
    description="Description",
    latitude=10.0,
    longitude=10.0,
    is_anonymous=False,
    status=ReportStatus.IN_PROGRESS,
    reporter_id=None,
    reporter=None,
)

@pytest.fixture
def seed_send_message_data() -> None:
    pass

# TC-7.1
def test_send_message_valid(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITH_RECIPIENT
    sender = AUTHORIZED_USER
    body = "Valid message"

    new_message = messaging_service.send_message(report, sender, body)

    assert new_message.report_id == report.id
    assert new_message.sender_id == sender.id
    assert new_message.body == body.strip()

# TC-7.2
def test_send_message_valid_trimmed(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITH_RECIPIENT
    sender = AUTHORIZED_USER
    body = " Valid message "

    new_message = messaging_service.send_message(report, sender, body)

    assert new_message.report_id == report.id
    assert new_message.sender_id == sender.id
    assert new_message.body == body.strip()

# TC-7.3
def test_send_message_unauthorized_user(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITH_RECIPIENT
    sender = UNAUTHORIZED_USER
    body = "Message from unauthorized user"

    with pytest.raises(AuthorizationError):
        messaging_service.send_message(report, sender, body)

# TC-7.4
def test_send_message_no_recipient(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITHOUT_RECIPIENT
    sender = AUTHORIZED_USER
    body = "Valid message"

    with pytest.raises(ValidationError):
        messaging_service.send_message(report, sender, body)

# TC-7.5
def test_send_message_empty_body(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITH_RECIPIENT
    sender = AUTHORIZED_USER
    body = ""

    with pytest.raises(ValidationError):
        messaging_service.send_message(report, sender, body)

# TC-7.6
def test_send_message_blank_body(seed_send_message_data: None) -> None:
    messaging_service = MessagingService()
    report = REPORT_WITH_RECIPIENT
    sender = AUTHORIZED_USER
    body = "  "

    with pytest.raises(ValidationError):
        messaging_service.send_message(report, sender, body)