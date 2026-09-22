from __future__ import annotations

import pytest
from unittest.mock import Mock

from participium.controllers.operator_controller import OperatorController, OperatorDashboardContext
from participium.models.enums import Role

@pytest.fixture
def mocked_dependencies():
    report_service = Mock()
    notification_service = Mock()
    report_service.list_pending_reports.return_value = []
    report_service.list_operator_reports.return_value = []
    notification_service.count_unread_message_notifications_by_report.return_value = {}
    return report_service, notification_service
 
 
@pytest.fixture
def operator_controller(mocked_dependencies):
    report_service, notification_service = mocked_dependencies
    return OperatorController(
        report_service=report_service,
        notification_service=notification_service,
    )


def make_user(user_id=1, role=Role.OPERATOR, category_id=5):
    u = Mock()
    u.id = user_id
    u.role = role
    u.category_id = category_id
    return u

def test_build_dashboard_admin_passes_filters_unchanged(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    admin = make_user(role=Role.ADMIN)
 
    operator_controller.build_dashboard(admin, filters={"date_from": "2024-01-01"})
 
    report_service.list_pending_reports.assert_called_once_with({"date_from": "2024-01-01"})
 
 
def test_build_dashboard_operator_injects_category_id(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    operator = make_user(role=Role.OPERATOR, category_id=7)
 
    operator_controller.build_dashboard(operator)
 
    call_args = report_service.list_pending_reports.call_args[0][0]
    assert call_args["category_id"] == 7
 
 
def test_build_dashboard_operator_merges_filters_with_category(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    operator = make_user(role=Role.OPERATOR, category_id=3)
 
    operator_controller.build_dashboard(operator, filters={"date_from": "2024-06-01"})
 
    call_args = report_service.list_pending_reports.call_args[0][0]
    assert call_args["category_id"] == 3
    assert call_args["date_from"] == "2024-06-01"
 
 
def test_build_dashboard_none_filters_does_not_crash(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    admin = make_user(role=Role.ADMIN)
 
    operator_controller.build_dashboard(admin, filters=None)
 
    report_service.list_pending_reports.assert_called_once()
 
 
def test_build_dashboard_other_role_skips_pending(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    citizen = make_user(role=Role.CITIZEN)
 
    result = operator_controller.build_dashboard(citizen)
 
    report_service.list_pending_reports.assert_not_called()
    assert result.pending_reports == []
 
 
def test_build_dashboard_unread_counts_queried_with_operator_id(operator_controller, mocked_dependencies):
    _, notification_service = mocked_dependencies
    operator = make_user(user_id=42, role=Role.OPERATOR)
 
    operator_controller.build_dashboard(operator)
 
    notification_service.count_unread_message_notifications_by_report.assert_called_once_with(42)
 

def test_assign_report_delegates_to_service(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    expected = Mock()
    report_service.assign_report.return_value = expected
    operator = make_user(role=Role.OPERATOR)
 
    result = operator_controller.assign_report(report_id=10, operator=operator)
 
    report_service.assign_report.assert_called_once_with(10, operator)
    assert result is expected
 

 
def test_update_status_delegates_to_service(operator_controller, mocked_dependencies):
    report_service, _ = mocked_dependencies
    expected = Mock()
    report_service.update_status.return_value = expected
    admin = make_user(role=Role.ADMIN)
 
    result = operator_controller.update_status(
        report_id=5,
        operator=admin,
        next_status_value="In Progress",
        note="Working on it",
    )
 
    report_service.update_status.assert_called_once_with(5, admin, "In Progress", "Working on it")
    assert result is expected