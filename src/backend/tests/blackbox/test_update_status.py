from __future__ import annotations

from participium.services.report_service import ReportService
import pytest
from participium.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from participium.models.enums import ReportStatus, Role
from participium.models.report import Report
from participium.models.user import User


VALID_REPORT_ID = 100
MISSING_REPORT_ID = 999999
INVALID_STATUS_VALUE = "INVALID_STATUS"

ADMIN_USER = User(
    id=1,
    username="admin.user",
    first_name="Admin",
    last_name="User",
    email="admin@example.com",
    password_hash="HASHED_PASSWORD_ADMIN",
    role=Role.ADMIN,
    is_active=True,
    is_email_verified=True,
)

UNAUTHORIZED_CITIZEN = User(
    id=2,
    username="citizen_1",
    first_name="Alan",
    last_name="Turing",
    email="Alan.Turing@example.com",
    password_hash="HASHED_PASSWORD_CITIZEN",
    role=Role.CITIZEN,
    is_active=True,
    is_email_verified=True,
)

AUTHORIZED_OPERATOR_CATEGORY_10 = User(
    id=3,
    username="operator_1",
    first_name="John",
    last_name="von Neumann",
    email="John.von.Neumann@example.com",
    password_hash="HASHED_PASSWORD_OP_A",
    role=Role.OPERATOR,
    category_id=10,
    is_active=True,
    is_email_verified=True,
)

AUTHORIZED_OPERATOR_CATEGORY_20 = User(
    id=4,
    username="operator_2",
    first_name="Linus",
    last_name="Torvalds",
    email="Linus.Torvalds@example.com",
    password_hash="HASHED_PASSWORD_OP_B",
    role=Role.OPERATOR,
    category_id=20,
    is_active=True,
    is_email_verified=True,
)

PENDING_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID,
    title="This report belongs to category 10",
    description="This is report description.",
    latitude=10.0,
    longitude=10.0,
    category_id=10,
    status=ReportStatus.PENDING_APPROVAL,
)

PENDING_REPORT_CATEGORY_20 = Report(
    id=VALID_REPORT_ID + 1,
    title="This report belongs to category 20",
    description="This is report description.",
    latitude=10.0,
    longitude=20.0,
    category_id=20,
    status=ReportStatus.PENDING_APPROVAL,
)

ASSIGNED_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID + 2,
    title="This report belongs to category 10 and is already assigned",
    description="This is report description.",
    latitude=10.1,
    longitude=10.1,
    category_id=10,
    status=ReportStatus.ASSIGNED,
)

REJECTED_REPORT_CATEGORY_10 = Report(
    id=VALID_REPORT_ID + 4,
    title="This report belongs to category 10 and is already rejected",
    description="This is report description.",
    latitude=10.2,
    longitude=10.2,
    category_id=10,
    status=ReportStatus.REJECTED,
)


@pytest.fixture
def seed_update_status_data() -> None:
    # Populate the system with the users and reports needed by
    # `ReportService.update_status`.
    pass

# TC-ID 5.1
def test_update_status_success_as_admin(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    updated_report = report_service.update_status(
        report_id=report_id,
        operator=operator,
        next_status_value=next_status_value,
        note=note,
    )

    assert isinstance(updated_report, Report)
    assert updated_report.id == PENDING_REPORT_CATEGORY_10.id
    assert updated_report.status == ReportStatus.ASSIGNED
    assert updated_report.category_id == PENDING_REPORT_CATEGORY_10.category_id

# TC-ID 5.2
def test_update_status_missing_report(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = MISSING_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    with pytest.raises(NotFoundError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.3
def test_update_status_unauthorized_user(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = UNAUTHORIZED_CITIZEN
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    with pytest.raises(AuthorizationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.4
def test_update_status_operator_outside_category(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = AUTHORIZED_OPERATOR_CATEGORY_20
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    with pytest.raises(AuthorizationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.5
def test_update_status_invalid_status_value(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = INVALID_STATUS_VALUE
    note = None

    with pytest.raises(ValidationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.6
def test_update_status_invalid_transition(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.IN_PROGRESS.value
    note = None

    with pytest.raises(ValidationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.7
def test_update_status_rejection_without_note(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.REJECTED.value
    note = None

    with pytest.raises(ValidationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

# TC-ID 5.8
def test_update_status_rejection_with_empty_note(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.REJECTED.value
    note = ""

    with pytest.raises(ValidationError):
        report_service.update_status(
            report_id=report_id,
            operator=operator,
            next_status_value=next_status_value,
            note=note,
        )

#  TC-ID 5.9
def test_update_status_success_as_operator_same_category(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = AUTHORIZED_OPERATOR_CATEGORY_10
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    updated_report = report_service.update_status(
        report_id=report_id,
        operator=operator,
        next_status_value=next_status_value,
        note=note,
    )

    assert isinstance(updated_report, Report)
    assert updated_report.id == PENDING_REPORT_CATEGORY_10.id
    assert updated_report.status == ReportStatus.ASSIGNED
    assert updated_report.category_id == PENDING_REPORT_CATEGORY_10.category_id

# TC-ID 5.10
def test_update_status_rejection_success(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID
    operator = ADMIN_USER
    next_status_value = ReportStatus.REJECTED.value
    note = "👍reason👍"

    updated_report = report_service.update_status(
        report_id=report_id,
        operator=operator,
        next_status_value=next_status_value,
        note=note,
    )

    assert isinstance(updated_report, Report)
    assert updated_report.id == PENDING_REPORT_CATEGORY_10.id
    assert updated_report.status == ReportStatus.REJECTED
    assert updated_report.rejection_reason is not None
    assert updated_report.rejection_reason is not ""

# TC-ID 5.11
def test_update_status_self_transition(seed_update_status_data: None) -> None:
    report_service = ReportService()
    report_id = VALID_REPORT_ID + 2
    operator = ADMIN_USER
    next_status_value = ReportStatus.ASSIGNED.value
    note = None

    updated_report = report_service.update_status(
        report_id=report_id,
        operator=operator,
        next_status_value=next_status_value,
        note=note,
    )

    assert isinstance(updated_report, Report)
    assert updated_report.id == PENDING_REPORT_CATEGORY_10.id
    assert updated_report.status == ReportStatus.ASSIGNED
    assert updated_report.category_id == PENDING_REPORT_CATEGORY_10.category_id

# IN SOME CASES IN WHICH THEY WILL RETURN THE UPDATED REPORT, SO DO I NEED TO CHANGE THE RETURN TYPE OF THE TEST METHODS FROM NONE TO REPORT?
# DOES IT NECESSARY ?