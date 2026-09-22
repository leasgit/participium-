from __future__ import annotations

from participium.models.enums import NotificationType, Role
import pytest

from participium.services.notification_service import NotificationService
#from test_wb_task06_smoke import *
from unittest.mock import Mock
from participium.models.user import User
from participium.models.report import Report

pytestmark = pytest.mark.whitebox


# Structural tests for NotificationService.notify_status_change belong here.
# The current runnable smoke check is kept in test_wb_task06_smoke.py.

def _user(*, user_id: int, username: str) -> User:
    return User(
        id=user_id,
        username=username,
        first_name="Alan",
        last_name="Turing",
        email="Alan.Turing@example.com",
        password_hash="HASHED_PASSWORD_CITIZEN",
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
    )

def _report(*, report_id: int) -> Report:
    return Report(
        id = report_id,
        title="This report belongs to category 10",
        description="This is report description.",
        latitude=10.0,
        longitude=10.0,
        category_id=10,
    )

@pytest.fixture
def notification_service_bundle() -> dict[str, object]:
    session = Mock()
    notification_repository = Mock()
    email_gateway = Mock()
    service = NotificationService(
        session=session,
        notification_repository=notification_repository,
        email_gateway=email_gateway,
    )
    create_notification = Mock()
    service.create_notification = create_notification
    report = _report(report_id=150)

    return {
        "create_notification": create_notification,
        "report": report,
        "service": service,
        "session": session,
        "notification_repository": notification_repository,
        "body": ""
    }

@pytest.fixture
def empty_recipients_case(notification_service_bundle: dict[str, object]) -> dict[str, object]:
    notification_service_bundle["recipients"] = []
    # build up an dict -> {"recipients" : [] }. Mock behave
    return notification_service_bundle

@pytest.fixture
def single_recipient_case(notification_service_bundle: dict[str, object]) -> dict[str, object]:
    recipient = _user(user_id=101, username="CITIZEN_01")
    notification_service_bundle["recipient"] = recipient
    notification_service_bundle["recipients"] = [ recipient]
    # {"recipient": recipient, "recipients" : [recipient] }
    # it is single
    return notification_service_bundle

@pytest.fixture
def multiple_recipients_case(notification_service_bundle: dict[str, object]) -> dict[str, object]:
    first_recipient = _user(user_id=101, username="CITIZEN_01")
    duplicated_by_id = _user(user_id=101, username="CITIZEN_1_D")
    user02_recipient = _user(user_id=102, username="CITIZEN_02")


    notification_service_bundle["first_recipient"] = first_recipient
    notification_service_bundle["duplicated_by_id"] = duplicated_by_id
    notification_service_bundle["user02_recipient"] = user02_recipient
    # in this case, it is multiple

    notification_service_bundle["recipients"] = [
        None, # user_id = None
        first_recipient,
        duplicated_by_id,
        user02_recipient
    ]
    # {"recipients": [None, ..., ....] , "None": None, ...}
    return notification_service_bundle

# this wb test is different goals from test_wb_mark_message_notifications.py
# cannot directly copy functions from it， but it is good for study and consider how to write wb

@pytest.mark.skip(reason="Disabled.")
def test_notify_status_change_with_no_recipients(
    empty_recipients_case: dict[str, object]
) -> None:
    service = empty_recipients_case["service"]
    create_notification = empty_recipients_case["create_notification"]
    recipients = empty_recipients_case["recipients"]
    report = empty_recipients_case["report"]
    body = empty_recipients_case["body"]

    result = service.notify_status_change(recipients=recipients, report=report, body=body)

    assert result is None
    create_notification.assert_not_called()

@pytest.mark.skip(reason="Disabled.")
def test_notify_status_change_with_one_recipients(
    single_recipient_case: dict[str, object]
) -> None:
    service = single_recipient_case["service"]
    create_notification = single_recipient_case["create_notification"]
    recipients = single_recipient_case["recipients"]
    recipient = single_recipient_case["recipient"]
    report = single_recipient_case["report"]
    body = single_recipient_case["body"]

    result = service.notify_status_change(recipients=recipients, report=report, body=body)

    assert result is None
    create_notification.assert_called_once_with(
        recipient,
        NotificationType.STATUS_CHANGE,
        f"Report #{report.id} status updated",
        body,
        report=report
    )

@pytest.mark.skip(reason="Disabled.")
def test_notify_status_change_with_multiple_recipients(
    multiple_recipients_case: dict[str, object]
) -> None:
    service = multiple_recipients_case["service"]
    create_notification = multiple_recipients_case["create_notification"]
    recipients = multiple_recipients_case["recipients"]
    first_recipient = multiple_recipients_case["first_recipient"]
    duplicated_by_id = multiple_recipients_case["duplicated_by_id"]
    user02_recipient = multiple_recipients_case["user02_recipient"]
    report = multiple_recipients_case["report"]
    body = multiple_recipients_case["body"]

    result = service.notify_status_change(recipients=recipients, report=report, body=body)

    assert result is None
    assert create_notification.call_count == 2
    create_notification.assert_any_call(
        first_recipient,
        NotificationType.STATUS_CHANGE,
        f"Report #{report.id} status updated",
        body,
        report=report
    )

    create_notification.assert_called_once_with(
        user02_recipient,
        NotificationType.STATUS_CHANGE,
        f"Report #{report.id} status updated",
        body,
        report=report
    )
