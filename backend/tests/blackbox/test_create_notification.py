from __future__ import annotations

import pytest

from participium.services.notification_service import NotificationService
from participium.models.user import User
from participium.models.report import Report
from participium.models.enums import ReportStatus
from participium.models.enums import NotificationType

NON_NULL_USER = User(
    id=101,
    username="maria.rossi",
    first_name="Maria",
    last_name="Rossi",
    email="maria.rossi@example.com",
    password_hash="HASHED_PASSWORD_101",
    is_active=True,
    is_email_verified=False,
)

USER_WITHOUT_EMAIL = User(
    id=102,
    username="mario.verdi",
    first_name="Mario",
    last_name="Verdi",
    email=None,
    password_hash="HASHED_PASSWORD_102",
    is_active=True,
    is_email_verified=False,
)

VALID_REPORT = Report(
    id=100,
    title="Report100",
    description="Description",
    latitude=10.0,
    longitude=10.0,
    is_anonymous=False,
    status=ReportStatus.IN_PROGRESS,
    reporter_id=101,
    reporter=NON_NULL_USER,
)

@pytest.fixture
def seed_create_notification_data() -> None:
    pass

# TC-9.1
def test_create_notification_system(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    non_null_user = NON_NULL_USER
    notification_type = NotificationType.SYSTEM
    notification_title = "title"
    notification_body = "body"

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, None)

    assert new_notification.user_id == non_null_user.id
    assert new_notification.report_id == None
    assert new_notification.type == notification_type
    assert new_notification.title == notification_title
    assert new_notification.body == notification_body
    assert new_notification.is_read == False
    assert new_notification.user == NON_NULL_USER
    assert new_notification.report == None

# TC-9.2
def test_create_notification_status_change(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    non_null_user = NON_NULL_USER
    notification_type = NotificationType.STATUS_CHANGE
    notification_title = "title"
    notification_body = "body"
    linked_report = VALID_REPORT

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification.user_id == non_null_user.id
    assert new_notification.report_id == linked_report.id
    assert new_notification.type == notification_type
    assert new_notification.report == linked_report

# TC-9.3
def test_create_notification_message(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    non_null_user = NON_NULL_USER
    notification_type = NotificationType.MESSAGE
    notification_title = "title"
    notification_body = "body"
    linked_report = VALID_REPORT

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification.user_id == non_null_user.id
    assert new_notification.report_id == linked_report.id
    assert new_notification.type == notification_type
    assert new_notification.report == linked_report

# TC-9.4
def test_create_notification_system_with_none_user(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    user = None
    notification_type = NotificationType.SYSTEM
    notification_title = "title"
    notification_body = "body"
    linked_report = None

    new_notification = notification_service.create_notification(user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification == None

# TC-9.5
def test_create_notification_status_change_with_none_user(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    user = None
    notification_type = NotificationType.STATUS_CHANGE
    notification_title = "title"
    notification_body = "body"
    linked_report = VALID_REPORT

    new_notification = notification_service.create_notification(user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification == None

# TC-9.6
def test_create_notification_message_with_none_user(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    user = None
    notification_type = NotificationType.MESSAGE
    notification_title = "title"
    notification_body = "body"
    linked_report = VALID_REPORT

    new_notification = notification_service.create_notification(user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification == None

# TC-9.7
def test_create_notification_with_empty_title(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    non_null_user = NON_NULL_USER
    notification_type = NotificationType.SYSTEM
    notification_title = ""
    notification_body = "body"
    linked_report = None

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification.title == ""

# TC-9.8
def test_create_notification_with_empty_body(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    non_null_user = NON_NULL_USER
    notification_type = NotificationType.SYSTEM
    notification_title = "title"
    notification_body = ""
    linked_report = None

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification.body == ""

# TC-9.9
def test_create_notification_with_user_without_email(seed_create_notification_data: None) -> None:
    notification_service = NotificationService()
    user = USER_WITHOUT_EMAIL
    notification_type = NotificationType.SYSTEM
    notification_title = "title"
    notification_body = "body"
    linked_report = None

    new_notification = notification_service.create_notification(non_null_user, notification_type, notification_title, notification_body, linked_report)

    assert new_notification.body != None
    assert new_notification.is_read == False