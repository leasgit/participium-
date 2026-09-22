from __future__ import annotations

import pytest

from unittest.mock import Mock

from participium.services.statistics_service import StatisticsService
from datetime import datetime

@pytest.mark.unit
def test_public_statistics_aggregation_logic():
    """
    Tests that public_statistics aggregates data correctly
    filtering only public reports.
    """

    # Mock reports and repository
    mock_repo = Mock()

    report_1 = Mock()
    report_1.category.name = "Roads"
    report_1.created_at = datetime(2026, 5, 1)

    report_2 = Mock()
    report_2.category.name = "Public Green"
    report_2.created_at = datetime(2026, 5, 1)
    
    report_3 = Mock()
    report_3.category.name = "Roads"
    report_3.created_at = datetime(2026, 5, 2)

    mock_repo.list_reports.return_value = [report_1, report_2, report_3]

    service = StatisticsService(mock_repo)

    # Call the method
    result = service.public_statistics(granularity="day")

    # Assertions
    assert result["total_reports"] == 3
    assert result["reports_by_category"] == {
        "Roads": 2,
        "Public Green": 1
    }
    assert result["trends"] == {
        "2026-05-01": 2,
        "2026-05-02": 1
    }
    mock_repo.list_reports.assert_called_once_with(public_only=True)

@pytest.mark.unit
def test_admin_statistics_reporter_identity_handling():
    """
    Verifies that admin statistics aggregates data correctly
    and handles reporter labels (deleted users included)
    """
    # Mocks
    mock_repo = Mock()

    test_user = Mock(username="TestUser", id=101)
    
    report_1 = Mock(reporter=test_user)
    report_1.category.name = "Roads"
    report_1.status.value = "In Progress"

    report_2 = Mock(reporter=None)
    report_2.category.name = "Public Green"
    report_2.status.value = "Pending Approval"

    mock_repo.list_all.return_value = [report_1, report_2]
    
    service = StatisticsService(mock_repo)

    # Call
    result = service.admin_statistics()

    # Assertions
    ## return active user label
    expected_label = "TestUser (101)"
    assert expected_label in result["reports_by_reporter"]
    assert result["reports_by_reporter"][expected_label] == 1

    ## return Deleted Citizen label for None reporter
    assert "Deleted Citizen" in result["reports_by_reporter"]
    assert result["reports_by_reporter"]["Deleted Citizen"] == 1

    ## complex aggregation (Reporter | Category | Status)
    expected_combined_key = "TestUser (101) | Roads | In Progress"
    assert result["reports_by_reporter_type_and_status"][expected_combined_key] == 1

    mock_repo.list_all.assert_called_once()

@pytest.mark.unit
def test_public_statistics_trends_granularity():
    """
    Tests that trends are correctly aggregated for week and month.
    """
    # Mocks
    mock_repo = Mock()
    report_1 = Mock(created_at=datetime(2026, 1, 15))
    report_2 = Mock(created_at=datetime(2026, 2, 20))
    mock_repo.list_reports.return_value = [report_1, report_2]

    service = StatisticsService(mock_repo)

    # Calls
    stats_month = service.public_statistics(granularity="month")
    stats_week = service.public_statistics(granularity="week")

    # Assertions
    assert stats_month["trends"] == {"2026-01": 1, "2026-02": 1}
    assert "2026-W03" in stats_week["trends"]
    assert "2026-W08" in stats_week["trends"]

@pytest.mark.unit
def test_admin_statistics_top_reporters_logic():
    """
    Test the calculation of top reporters (1% and 5%)
    """
    
    # Mocks
    mock_repo = Mock()

    reports = []
    for i in range(10):
        u = Mock(username=f"user_{i}", id=i)
        r = Mock(reporter=u)
        r.category.name = "Pollution"
        r.status.value = "Resolved"
        reports.append(r)

    mock_repo.list_all.return_value = reports
    service = StatisticsService(mock_repo)

    # Call
    result = service.admin_statistics()

    # Assertions
    assert "top_1_percent_by_type" in result
    assert result["top_1_percent_by_type"]["Pollution"] >= 1
    assert result["top_5_percent_by_type"]["Pollution"] >= 1

@pytest.mark.unit
def test_statistics_with_no_data():
    """
    Tests that service does not crash if there are no reports in the system
    """

    # Mocks
    mock_repo = Mock()
    mock_repo.list_reports.return_value = []
    mock_repo.list_all.return_value = []

    service = StatisticsService(mock_repo)

    # Calls
    pub_stats = service.public_statistics()
    admin_stats = service.admin_statistics()

    # Assertions
    assert pub_stats["total_reports"] == 0
    assert pub_stats["reports_by_category"] == {}
    assert admin_stats["top_1_percent_by_type"] == {}
