from __future__ import annotations

import pytest

from participium.services.messaging_service import MessagingService


pytestmark = pytest.mark.whitebox


# Structural tests for MessagingService._resolve_recipient belong here.
# The current runnable smoke check is kept in test_wb_task06_smoke.py.


from unittest.mock import Mock
from participium.models.enums import Role

pytestmark = pytest.mark.whitebox

#helpers

def _make_sender(role: Role) -> Mock:
    sender = Mock()
    sender.role = role
    return sender

def _make_message(sender_role: Role | None) -> Mock:
    message = Mock()
    if sender_role is None:
        message.sender = None
    else:
        message.sender = Mock()
        message.sender.role = sender_role
    return message

def _make_status_event(changed_by_role: Role | None) -> Mock:
    event = Mock()
    if changed_by_role is None:
        event.changed_by = None
    else:
        event.changed_by = Mock()
        event.changed_by.role = changed_by_role
    return event

def _make_report(status_history: list) -> Mock:
    report = Mock()
    report.id = 1
    report.reporter = Mock()
    report.status_history = status_history
    return report
 

#fixture

@pytest.fixture
def messaging_service_bundle() -> dict[str, object]:
    session = Mock()
    message_repository = Mock()
    report_repository = Mock()
    notification_service = Mock()
    service = MessagingService(
        session=session,
        report_repository=report_repository,
        message_repository=message_repository,
        notification_service=notification_service,
    )
    return {
        "service": service,
        "message_repository": message_repository,
    }

#P1 - return report.reportersender.role is an ADMIN or OPERATOR -> return report.reporter
class TestP1SenderIsStaff:
 
 #if sender is admin
    def test_sender_is_admin_returns_reporter( 
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.ADMIN)
        report = _make_report(status_history=[])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is report.reporter
        message_repository.list_for_report.assert_not_called()
 
 #if sender is operator
    def test_sender_is_operator_returns_reporter(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.OPERATOR)
        report = _make_report(status_history=[])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is report.reporter
        message_repository.list_for_report.assert_not_called()
 
 

# P2 — sender.role not an ADMIN or OPERATOR, messages list has one message sent by an ADMIN or OPERATOR -> return message.sender
 
class TestP2QualifyingMessageExists:
 
    def test_returns_message_sender_when_staff_sent_a_message(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
        qualifying_message = _make_message(sender_role=Role.ADMIN)
        message_repository.list_for_report.return_value = [qualifying_message]
 
        report = _make_report(status_history=[])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is qualifying_message.sender
 
 
# P3 - sender.role not an ADMIN or OPERATOR, messages list not empty but no qualified message sender, 
#      status list not empty but no qualifying status event changed_by -> return None

class TestP3BothLoopsExhausted:
 
    def test_returns_none_when_no_qualifying_sender_or_status_event(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
 
        message_repository.list_for_report.return_value = [
            _make_message(sender_role=Role.CITIZEN),
            _make_message(sender_role=Role.CITIZEN),
        ]
 
        report = _make_report(status_history=[
            _make_status_event(changed_by_role=Role.CITIZEN),
            _make_status_event(changed_by_role=Role.CITIZEN),
        ])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is None
 
 
# P4 - sender.role not an ADMIN or OPERATOR, messages list not empty but no qualified message sender, 
#      status list not empty but has one event with ADMIN/OPERATOR changed_by -> return status_event.changed_by

class TestP4QualifyingStatusEventExists:
 
    def test_returns_changed_by_when_staff_changed_status(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
 
        message_repository.list_for_report.return_value = [
            _make_message(sender_role=Role.CITIZEN),
        ]
 
        qualifying_event = _make_status_event(changed_by_role=Role.ADMIN)
        report = _make_report(status_history=[qualifying_event])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is qualifying_event.changed_by
 
 
# P5 - sender.role not an ADMIN or OPERATOR, messages list not empty and has one message where sender exists
#      but not ADMIN/OPERATOR -> continues to status loop

class TestP5MessageSenderExistsButNotStaff:
 
    def test_citizen_message_sender_is_not_returned(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
 
        message_repository.list_for_report.return_value = [
            _make_message(sender_role=Role.CITIZEN),
        ]
 
        report = _make_report(status_history=[])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is None
 
 
# P6 - sender.role not an ADMIN or OPERATOR, status list has one event where changed_by exists but role not ADMIN/OPERATOR -> returns None

class TestP6ChangedByExistsButNotStaff:
 
    def test_citizen_changed_by_is_not_returned(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
        message_repository.list_for_report.return_value = []
 
        report = _make_report(status_history=[
            _make_status_event(changed_by_role=Role.CITIZEN),
        ])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is None
 
 
# PL - sender.role not an ADMIN or OPERATOR, message list empty, status list empty -> returns None

class TestPLBothListsEmpty:
 
    def test_returns_none_when_both_lists_are_empty(
        self, messaging_service_bundle: dict[str, object]
    ) -> None:
        service = messaging_service_bundle["service"]
        message_repository = messaging_service_bundle["message_repository"]
 
        sender = _make_sender(Role.CITIZEN)
        message_repository.list_for_report.return_value = []
 
        report = _make_report(status_history=[])
 
        result = service._resolve_recipient(report, sender)
 
        assert result is None
 