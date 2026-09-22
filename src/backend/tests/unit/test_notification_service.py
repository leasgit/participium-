from __future__ import annotations

import pytest

from unittest.mock import Mock

from participium.models.enums import NotificationType
from participium.services.notification_service import NotificationService
from participium.core.exceptions import AuthorizationError, NotFoundError

# --- TESTS FOR CREATION AND EMAIL ---

@pytest.mark.unit
def test_create_notification_email_success():
    """
    Tests the creation of a notification with email send success
    """

    # Mocks
    mock_repo = Mock()
    mock_gateway = Mock()
    service = NotificationService(notification_repository=mock_repo, email_gateway=mock_gateway)

    user = Mock(
        id=101,
        email="test@test.com",
        email_notifications_enabled=True
    )
    report = Mock(id=10)

    # Calls
    result = service.create_notification(user, NotificationType.STATUS_CHANGE, "Title", "Body", report)

    # Assertions
    assert result is not None
    assert result.user_id == 101
    assert result.report_id == 10
    mock_repo.add.assert_called_once()
    mock_gateway.send.assert_called_once_with("test@test.com", "Title", "Body")

@pytest.mark.unit
def test_create_notification_email_failure_is_swallowed():
    """
    If send email fails, the in-platform notification must be still created
    without raising exceptions
    """

    # Mocks
    mock_repo = Mock()
    mock_gateway = Mock()
    mock_gateway.send.side_effect = Exception("SMTP Server Down")

    service = NotificationService(notification_repository=mock_repo, email_gateway=mock_gateway)
    user = Mock(
        id=101,
        email="test@test.com",
        email_notifications_enabled=True
    )

    # Call
    result = service.create_notification(user, NotificationType.STATUS_CHANGE, "Title", "Body")

    # Assertions
    assert result is not None
    mock_repo.add.assert_called_once()

@pytest.mark.unit
def test_create_notification_for_none_user():
    """
    Tests boundary case: None user
    """

    service = NotificationService()
    result = service.create_notification(None, NotificationType.STATUS_CHANGE, "Title", "Body")
    assert result is None

# --- TESTS FOR DEDUPLICATION ---

@pytest.mark.unit
def test_notify_status_change_deduplication():
    """
    Tests that duplicated users and None are ignored by the method notify_status_change
    """

    # Mocks
    service = NotificationService(notification_repository=Mock(), email_gateway=Mock())
    service.create_notification = Mock()

    u1 = Mock(id=101)
    u2 = Mock(id=102)
    report = Mock()

    recipients = [u1, None, u2, u1]

    # Calls
    service.notify_status_change(recipients, report, "Body")

    # Assertions
    assert service.create_notification.call_count == 2

# --- TESTS FOR AGGREGATION ---
@pytest.mark.unit
def test_count_unread_message_notifications_by_report():
    """
    Tests that aggregation by report_id works and ignore None
    """

    # Mocks
    mock_repo = Mock()
    n1 = Mock(report_id=10)
    n2 = Mock(report_id=10)
    n3 = Mock(report_id = None)
    mock_repo.list_unread_message_notifications.return_value = [n1, n2, n3]

    service = NotificationService(notification_repository=mock_repo)

    # Calls
    counts = service.count_unread_message_notifications_by_report(user_id=101)

    # Assertions
    assert counts == {10: 2}

# --- TESTS FOR EXCEPTIONS AND SECURITY ---

@pytest.mark.unit
def test_get_user_notification_not_found():
    """
    Tests NotFoundError raise if notification does not exits
    """
    
    # Mocks
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = None
    service = NotificationService(notification_repository=mock_repo)

    #Assertions
    with pytest.raises(NotFoundError):
        service.get_user_notification(user_id=101, notification_id=10)

@pytest.mark.unit
def test_get_user_notification_authorization_error():
    """
    Tests raise AuthorizationError if the user is not the owner of the notification
    """

    # Mocks
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = Mock(user_id=102)
    service = NotificationService(notification_repository=mock_repo)

    # Assertions
    with pytest.raises(AuthorizationError):
        service.get_user_notification(user_id=101, notification_id=10)