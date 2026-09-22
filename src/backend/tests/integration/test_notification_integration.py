from __future__ import annotations

import pytest

from participium.models.category import Category
from participium.models.enums import NotificationType, ReportStatus, Role
from participium.models.notification import Notification
from participium.models.report import Report
from participium.models.user import User
from participium.repositories.notification_repository import NotificationRepository

@pytest.mark.integration
def test_notification_repository_crud_lifecycle(db_session):
    """
    Tests the saving and getting of a notification.
    """

    # Arrange
    user = User(username="admin",
                 first_name="Admin",
                 last_name="User",
                 role=Role.ADMIN,
                 password_hash="HASHED_PASSWORD",
                 email="admin@test.com",
                 is_active=True,
                 is_email_verified=True)
    db_session.add(user)
    db_session.commit()

    repo = NotificationRepository(db_session)

    # Act
    notification = Notification(
        user_id=user.id,
        type=NotificationType.STATUS_CHANGE,
        title="Title",
        body="Body",
        is_read=False
    )
    repo.add(notification)
    db_session.commit()
    saved_notifications = repo.list_for_user(user.id)

    # Assertions
    assert len(saved_notifications) == 1
    assert saved_notifications[0].title == "Title"
    assert saved_notifications[0].body == "Body"
    assert saved_notifications[0].is_read is False

@pytest.mark.integration
def test_list_unread_message_notifications_filtering(db_session):
    """
    Tests that the query to the database filter for unread messages correctly:
    - Only notifications type MESSAGE
    - Only unread notifications
    - Owned by the right user
    """

    # Arrange
    user = User(username="admin",
                 first_name="Admin",
                 last_name="User",
                 role=Role.ADMIN,
                 password_hash="HASHED_PASSWORD",
                 email="admin@test.com",
                 is_active=True,
                 is_email_verified=True
    )
    category = Category(name="Roads", is_active=True)
    db_session.add_all([user, category])
    db_session.commit()

    report = Report(
        title="Title",
        description="Description",
        category=category,
        reporter=user,
        status=ReportStatus.IN_PROGRESS
    )
    
    repo = NotificationRepository(db_session)

    n1 = Notification(
            user_id=user.id,
            report_id=report.id,
            type=NotificationType.MESSAGE,
            title="Msg 1",
            body="...",
            is_read=False
        )
    
    n2 = Notification(
            user_id=user.id,
            report_id=report.id,
            type=NotificationType.MESSAGE,
            title="Msg 2",
            body="...",
            is_read=True
        )

    n3 = Notification(
            user_id=user.id,
            report_id=report.id,
            type=NotificationType.STATUS_CHANGE,
            title="Status",
            body="...",
            is_read=False
        )
    
    db_session.add_all([n1, n2, n3])
    db_session.commit()

    # Act
    unread_messages = repo.list_unread_message_notifications(user_id=user.id, report_id=report.id)

    # Assert
    assert len(unread_messages) == 1
    assert unread_messages[0].title == "Msg 1"

@pytest.mark.integration
def test_get_by_id_returns_correct_notification(db_session):
    """
    Tests that get_by_id returns the correct entities or None if not exists
    """

    # Arrange
    user = User(username="admin",
                 first_name="Admin",
                 last_name="User",
                 role=Role.ADMIN,
                 password_hash="HASHED_PASSWORD",
                 email="admin@test.com",
                 is_active=True,
                 is_email_verified=True
    )
    db_session.add(user)
    db_session.commit()

    repo = NotificationRepository(db_session)
    n = Notification(user_id=user.id, type=NotificationType.SYSTEM, title="Sys", body="...", is_read=False)
    db_session.add(n)
    db_session.commit()

    # Act
    found_notification = repo.get_by_id(n.id)
    not_found_notification = repo.get_by_id(999)

    # Assert
    assert found_notification is not None
    assert found_notification.id == n.id
    assert not_found_notification is None
