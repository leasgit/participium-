from __future__ import annotations

from participium.services.report_service import ReportService

import pytest
from participium.models.enums import ReportStatus
from participium.models.report import Report
from participium.core.utils import parse_date

VALID_REPORT_ID = 100
MISSING_REPORT_ID = 999999
INVALID_STATUS_VALUE = "INVALID_STATUS"

X_DATETIME = parse_date("2025-01-01T00:00:00Z")
Y_DATETIME = parse_date("2025-06-30T23:23:59Z")

PENDING_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID,
    title="This report belongs to category 10",
    description="This is report description.",
    latitude=10.0,
    longitude=10.0,
    category_id=10,
    status=ReportStatus.PENDING_APPROVAL,
    created_at=parse_date("2025-01-02T12:00:00Z"),
)

PENDING_REPORT_CATEGORY_20 = Report(
    id=VALID_REPORT_ID + 1,
    title="This report belongs to category 20",
    description="This is report description.",
    latitude=10.0,
    longitude=20.0,
    category_id=20,
    status=ReportStatus.PENDING_APPROVAL,
    created_at=parse_date("2025-01-03T12:00:00Z"),
)

ASSIGNED_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID + 2,
    title="This report belongs to category 10 and is already assigned",
    description="This is report description.",
    latitude=10.1,
    longitude=10.1,
    category_id=10,
    status=ReportStatus.ASSIGNED,
    created_at=parse_date("2026-01-03T12:00:00Z"),
)

REJECTED_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID + 3,
    title="This report belongs to category 10 and is already rejected",
    description="This is report description.",
    latitude=10.2,
    longitude=10.2,
    category_id=10,
    status=ReportStatus.REJECTED,
    created_at=parse_date("2023-01-03T12:00:00Z"),
)

RESOLVED_REPORT_CATEGORY_20 = Report(
    id=VALID_REPORT_ID + 4,
    title="This report belongs to category 20 and is already resolved",
    description="This is report description.",
    latitude=10.3,
    longitude=10.3,
    category_id=20,
    status=ReportStatus.RESOLVED,
    created_at=parse_date("2025-06-30T23:23:59Z"),
)

@pytest.fixture
def seed_update_status_data() -> None:
    # Populate the system with the users and reports needed by
    # `ReportService.update_status`.
    
    # suggested dataset:
    # - the relative database for reports
    pass

# TC-ID 6.1
def test_list_public_reports_all_visible_ascending(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=None,
        date_to=None,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        REJECTED_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_20.id,
        RESOLVED_REPORT_CATEGORY_20.id,
        ASSIGNED_REPORT_CATEGORY_10.id,
    ]

# TC-ID 6.2
def test_list_public_reports_all_visible_descending(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=None,
        date_to=None,
        sort="desc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        ASSIGNED_REPORT_CATEGORY_10.id,
        RESOLVED_REPORT_CATEGORY_20.id,
        PENDING_REPORT_CATEGORY_20.id,
        PENDING_REPORT_CATEGORY_10.id,
        REJECTED_REPORT_CATEGORY_10.id,
    ]

# TC-ID 6.3
def test_list_public_reports_filtered_by_category(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=10,
        status=None,
        date_from=None,
        date_to=None,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        ASSIGNED_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_10.id,
        REJECTED_REPORT_CATEGORY_10.id,
    ]

# TC-ID 6.4
def test_list_public_reports_filtered_by_status(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=ReportStatus.PENDING_APPROVAL,
        date_from=None,
        date_to=None,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        PENDING_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_20.id,
    ]

# TC-ID 6.5
def test_list_public_reports_filtered_by_dateFrom(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=X_DATETIME,
        date_to=None,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        PENDING_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_20.id,
        ASSIGNED_REPORT_CATEGORY_10.id,
        RESOLVED_REPORT_CATEGORY_20.id,
    ]

# TC-ID 6.6
def test_list_public_reports_filtered_by_dateTo(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=None,
        date_to=Y_DATETIME,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        PENDING_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_20.id,
        REJECTED_REPORT_CATEGORY_10.id,
        RESOLVED_REPORT_CATEGORY_20.id,
    ]

# TC-ID 6.7
def test_list_public_reports_filtered_by_time_range(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=X_DATETIME,
        date_to=Y_DATETIME,
        sort="asc")
    
    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        PENDING_REPORT_CATEGORY_10.id,
        PENDING_REPORT_CATEGORY_20.id,
        RESOLVED_REPORT_CATEGORY_20.id
    ]

# TC-ID 6.8
def test_list_public_reports_filtered_by_all(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=20,
        status=ReportStatus.PENDING_APPROVAL,
        date_from=X_DATETIME,
        date_to=Y_DATETIME,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert [report.id for report in public_reports] == [
        PENDING_REPORT_CATEGORY_20.id
    ]

# TC-ID 6.9
def test_list_public_reports_no_match(seed_public_reports_data: None) -> None:
    report_service = ReportService()

    public_reports = report_service.list_public_reports(
        category_id=MISSING_REPORT_ID,
        status=ReportStatus.PENDING_APPROVAL,
        date_from=X_DATETIME,
        date_to=Y_DATETIME,
        sort="asc",
    )

    assert isinstance(public_reports, list)
    assert len(public_reports) == 0