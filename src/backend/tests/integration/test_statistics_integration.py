from __future__ import annotations

import pytest

from datetime import datetime
from participium.database import open_connection, close_connection, create_all, get_session
from participium.models.enums import Role
from participium.models.report import Report
from participium.models.category import Category
from participium.models.user import User
from participium.repositories.report_repository import ReportRepository
from participium.services.statistics_service import StatisticsService
from participium.models.enums import ReportStatus

@pytest.mark.integration
def test_statistics_with_real_database(db_session):
    """
    Tests that the service reads correctly data from the DB.
    """

    # Arrange
    admin = User(username="admin",
                 first_name="Admin",
                 last_name="User",
                 role=Role.ADMIN,
                 password_hash="HASHED_PASSWORD",
                 email="admin@test.com",
                 is_active=True,
                 is_email_verified=True)
    c1 = Category(name="Public Green", is_active=True)
    db_session.add_all([admin, c1])
    db_session.commit()

    r1 = Report(
        title="Fallen tree",
        description="A big tree fell in the street.",
        category=c1,
        reporter=admin,
        status="Resolved",
        latitude=45.0703,
        longitude=7.6869,
        created_at=datetime(2026, 5, 1)
    )
    db_session.add(r1)
    db_session.commit()

    # Act
    repo = ReportRepository(db_session)
    service = StatisticsService(repo)

    pub_stats = service.public_statistics()

    # Assert
    assert pub_stats["total_reports"] == 1
    assert pub_stats["reports_by_category"]["Public Green"] == 1
    assert pub_stats["trends"] == {
        "2026-05-01": 1
    }

@pytest.mark.integration
def test_public_statistics_privacy_filter(db_session):
    """
    Verify that public statistics does not include reports
    in private statuses
    """

    # Arrange
    reporter = User(username="admin",
        first_name="Admin",
        last_name="User",
        role=Role.ADMIN,
        password_hash="HASHED_PASSWORD",
        email="admin@test.com",
        is_active=True,
        is_email_verified=True
    )
    category = Category(name="Trash", is_active=True)
    db_session.add_all([reporter, category])
    db_session.commit()

    public_report = Report(
        title="Public_report",
        description="Test_description",
        category=category,
        reporter=reporter,
        status=ReportStatus.ASSIGNED,
        latitude=45.0, longitude=7.0,
        created_at=datetime(2026, 5, 1)
    )

    private_report = Report(
        title="Private_report",
        description="test_description",
        category=category,
        reporter=reporter,
        status=ReportStatus.PENDING_APPROVAL,
        latitude=45.1, longitude=7.1,
        created_at=datetime(2026, 5, 1)
    )

    db_session.add_all([public_report, private_report])
    db_session.commit()

    # Act
    repo = ReportRepository(db_session)
    service = StatisticsService(repo)

    pub_stats = service.public_statistics()

    # Assert
    assert pub_stats["total_reports"] == 1
    assert pub_stats["reports_by_category"]["Trash"] == 1
    assert pub_stats["trends"]["2026-05-01"] == 1
