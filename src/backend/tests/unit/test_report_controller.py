from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock
import pytest
from participium.models.enums import ReportStatus
from werkzeug.datastructures import FileStorage

from participium.controllers.report_controller import ReportController, ReportDetailContext


def make_controller():
    report_service = Mock()
    messaging_service = Mock()
    notification_service = Mock()

    controller = ReportController(
        report_service=report_service,
        messaging_service=messaging_service,
        notification_service=notification_service
    )

    return controller, report_service, messaging_service, notification_service

@pytest.mark.unit
def test_list_public_reports_delegates_to_report_service():
    controller, report_service,_,_ = make_controller()
    reports = [Mock(id=1), Mock(id=2)]
    date_from = datetime(2026, 5, 1)
    date_to = datetime(2026, 5, 7)

    report_service.list_public_reports.return_value = reports

    result = controller.list_public_reports(
        category_id = 10,
        status=ReportStatus.IN_PROGRESS,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

    assert result == reports
    report_service.list_public_reports.assert_called_once_with(
        category_id = 10,
        status=ReportStatus.IN_PROGRESS,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

@pytest.mark.unit
def test_list_user_reports_delegates_to_report_service():
    controller, report_service, _, _ = make_controller()
    user = Mock(id=101)

    reports = [Mock(id=1)]
    report_service.list_user_reports.return_value = reports

    result = controller.list_user_reports(user)

    assert result == reports
    report_service.list_user_reports.assert_called_once_with(user)

@pytest.mark.unit
def test_build_detail_context():
    controller, report_service, messaging_service, notification_service = make_controller()
    user = Mock(id=101)
    report = Mock(id=55)

    report_service.get_accessible_report.return_value = report
    messaging_service.can_access_thread.return_value = True

    result = controller.build_detail_context(report_id=55, user=user)

    assert result == ReportDetailContext(report=report, can_access_messages=True)
    report_service.get_accessible_report.assert_called_once_with(55, user)
    messaging_service.can_access_thread.assert_called_once_with(report, user)
    notification_service.mark_report_message_notifications_as_read.assert_called_once_with(101, 55)

@pytest.mark.unit
@pytest.mark.parametrize(
    "user, can_access_messages",
    [
        (None, True),
        (Mock(id=101), False)
    ]
)

@pytest.mark.unit
def test_build_detail_context_does_not_mark_notification(user, can_access_messages):
    controller, report_service, messaging_service, notification_service = make_controller()
    report = Mock(id=55)

    report_service.get_accessible_report.return_value = report
    messaging_service.can_access_thread.return_value = can_access_messages

    result = controller.build_detail_context(report_id=55, user=user)

    assert result == ReportDetailContext(report=report, can_access_messages=can_access_messages)
    report_service.get_accessible_report.assert_called_once_with(55, user)
    messaging_service.can_access_thread.assert_called_once_with(report, user)
    notification_service.mark_report_message_notifications_as_read.assert_not_called()

@pytest.mark.unit
def test_report_service_create_report():
    controller, report_service, _, _ = make_controller()

    reporter = Mock(id=101)
    photos = [Mock(spec=FileStorage)]
    created_reported = Mock(id=77)

    report_service.create_report.return_value = created_reported

    result = controller.create_report(
        reporter=reporter,
        category_id = "3",
        title = ".....",
        description = "",
        latitude = "10.1",
        longitude = "20.1",
        photos=photos,
        is_anonymous = True
    )

    assert result == created_reported
    report_service.create_report.assert_called_once_with(
        reporter=reporter,
        category_id = "3",
        title = ".....",
        description = "",
        latitude = "10.1",
        longitude = "20.1",
        photos=photos,
        is_anonymous = True
    )

@pytest.mark.unit
def test_follow_report_to_report_service():
    controller, report_service, _, _ = make_controller()
    user = Mock(id=101)
    report = Mock(id=55)
    report_service.follow_report.return_value = report

    result = controller.follow_report(report_id=55, user=user)

    assert result == report
    report_service.follow_report.assert_called_once_with(55, user)

@pytest.mark.unit
def test_unfollow_report_to_report_service():
    controller, report_service, _, _ = make_controller()
    user = Mock(id=101)
    report = Mock(id=55)
    report_service.unfollow_report.return_value = report

    result = controller.unfollow_report(report_id=55, user=user)

    assert result == report
    report_service.unfollow_report.assert_called_once_with(55, user)

@pytest.mark.unit
def test_report_service_export_rows():
    controller, report_service, _, _ = make_controller()
    date_from = datetime(2026, 5, 1)
    date_to = datetime(2026, 5, 7)    

    rows = [{ "id": 1,
            "title": ".......",
            "status": "In Progress",
            "latitude": 10.1,
            "longitude": 20.2,}]
    
    report_service.export_rows.return_value = rows

    result = controller.export_rows(
        category_id = 10,
        status = ReportStatus.IN_PROGRESS,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

    assert result == rows
    report_service.export_rows.assert_called_once_with(
        category_id = 10,
        status = ReportStatus.IN_PROGRESS,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

@pytest.mark.unit
def test_messaging_service_list_messages():
    controller, _, messaging_service,_ = make_controller()
    report = Mock(id=55)
    user = Mock(id=101)
    messages = [Mock(id=1), Mock(id=2)]

    messaging_service.list_messages.return_value = messages

    result = controller.list_messages(report,user)

    assert result == messages
    messaging_service.list_messages.assert_called_once_with(report, user)

@pytest.mark.unit
def test_send_message_delegates_to_messaging_service():
    controller, _, messaging_service, _ = make_controller()
    report = Mock(id=55)
    sender = Mock(id=101)
    message = Mock(id=1, body="Hello")

    messaging_service.send_message.return_value = message

    result = controller.send_message(report, sender, "Hello")

    assert result == message
    messaging_service.send_message.assert_called_once_with(report, sender, "Hello")