from __future__ import annotations
from participium.models.report import Report, ReportFollower, ReportPhoto, ReportStatusHistory
from participium.core.exceptions import NotFoundError, AuthorizationError, ValidationError
import pytest
from unittest.mock import Mock

from participium.services import ReportService
from participium.models.enums import ReportStatus, Role
from types import SimpleNamespace
from datetime import datetime


def make_service() -> ReportService:
   
    return ReportService(
        session = Mock(),
        report_repository = Mock(),
        category_repository = Mock(),
        storage_service = Mock(),
        notification_service = Mock()
    )

def user(user_id: int = 1, role: Role = Role.CITIZEN, category_id: int | None = None):
    return SimpleNamespace(id=user_id, role=role, category_id=category_id)

def category(category_id: int = 10, name: str = "Roads", is_active: bool = True):
    return SimpleNamespace(id=category_id, name=name, is_active=is_active)

def follower(follower_user):
    return SimpleNamespace(user=follower_user)

def report(report_id: int =50,
           status: ReportStatus = ReportStatus.ASSIGNED,
           reporter_id: int =1,
           category_id: int = 10):
    return SimpleNamespace(
        id=report_id,
        title="BROKEN",
        description="......",
        latitude=20.0,
        longitude=20.0,
        status=status,
        reporter_id=reporter_id,
        category_id=category_id,
        category=category(category_id),
        reporter=user(reporter_id),
        followers=[],
        rejection_reason=None,
        created_at=datetime(2026, 1, 2, 3, 4, 5)
    )


@pytest.mark.unit 
def test_list_public_reports():
    service = make_service()
    expected_reports = [report()]
    service.report_repository.list_reports.return_value = expected_reports
    date_from = datetime(2026, 1, 1)
    date_to = datetime(2026,1, 31)

    result = service.list_public_reports(
        category_id=10,
        status=ReportStatus.ASSIGNED,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

    assert result == expected_reports
    service.report_repository.list_reports.assert_called_once_with(
        public_only=True,
        category_id=10,
        status = ReportStatus.ASSIGNED,
        date_from=date_from,
        date_to=date_to,
        sort="asc"
    )

@pytest.mark.unit
def test_list_user_reports_return_user_id():
    service = make_service()
    reports = [report()]
    service.report_repository.list_user_reports.return_value = reports

    result = service.list_user_reports(user())

    assert result == reports
    service.report_repository.list_user_reports.assert_called_once_with(1)
    
@pytest.mark.unit
def test_get_report_return_report_success():
    service = make_service()
    expected_report = report()

    service.report_repository.get_by_id.return_value = expected_report
    result = service.get_report(report_id=50)

    assert result == expected_report

@pytest.mark.unit
def test_get_report_return_NotFound():
    service = make_service()
    # except_report = report()
    service.report_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Report not found"):
        service.get_report(404)

@pytest.mark.unit
def test_get_accessible_report_return_report():
    service = make_service()
    expected_report = report(status=ReportStatus.RESOLVED)
    service.report_repository.get_by_id.return_value = expected_report

    result = service.get_accessible_report(report_id=50)

    assert result == expected_report

@pytest.mark.unit
def test_get_accessible_report_return_userNone():
    service = make_service()
    expected_report = report(status=ReportStatus.PENDING_APPROVAL)
    service.report_repository.get_by_id.return_value = expected_report

    with pytest.raises(AuthorizationError):
        service.get_accessible_report(expected_report.id)

@pytest.mark.parametrize(
    ("current_user", "private_report"),
    [
        (user(1, Role.CITIZEN), report(status=ReportStatus.PENDING_APPROVAL, reporter_id=1)),
        (user(2, Role.ADMIN), report(status=ReportStatus.PENDING_APPROVAL, reporter_id=1)),
        (user(3, Role.OPERATOR, category_id=10), report(status=ReportStatus.PENDING_APPROVAL, reporter_id=1, category_id=10))
    ]
)

@pytest.mark.unit
def test_get_accessible_report_allows_reporter_admin_and_matching_operator(current_user, private_report):
    service = make_service()
    service.report_repository.get_by_id.return_value = private_report

    assert service.get_accessible_report(private_report.id, current_user) == private_report

@pytest.mark.unit
def test_get_accessible_report_rejects_user_without_access_private():
    service = make_service()
    expected_report = report(status=ReportStatus.PENDING_APPROVAL)
    service.report_repository.get_by_id.return_value = expected_report

    with pytest.raises(AuthorizationError):
        service.get_accessible_report(expected_report.id, user(Role.OPERATOR, category_id=12))

def photo(filename: str | None = "photo.jpg"):
    return SimpleNamespace(filename=filename, content_type="image/jpeg")

@pytest.mark.unit
def test_create_report_persists_report_photos_and_initial_status_history():
    service = make_service()
    reporter = user(8)
    active_category = category(12, "roads")
    created_report = report(77, status=ReportStatus.PENDING_APPROVAL, reporter_id=8, category_id=12)
    photos = [photo("fix_before.jpg"), photo(None), None, photo("fix_after.jpg")]
    service.category_repository.get_by_id.return_value = active_category
    service.storage_service.save.side_effect = ["reports/fix_before.jpg", "reports/fix_after.jpg"]
    service.report_repository.get_by_id.return_value = created_report

    def assign_id(added_report):
        added_report.id = created_report.id

    service.report_repository.add.side_effect = assign_id

    result = service.create_report(
        reporter=reporter,
        category_id="12",
        title="roads",
        description=".........",
        latitude="20.0",
        longitude="20.0",
        photos=photos,
        is_anonymous=True,
    )

    assert result == created_report
    added_report = service.report_repository.add.call_args.args[0]
    assert isinstance(added_report, Report)
    assert added_report.title == "roads"
    assert added_report.description == "........."
    assert added_report.latitude == 20.0
    assert added_report.longitude == 20.0
    assert added_report.is_anonymous is True
    assert added_report.status == ReportStatus.PENDING_APPROVAL
    assert added_report.reporter_id == reporter.id
    assert added_report.category_id == active_category.id
    assert service.storage_service.save.call_count == 2
    added_photos = [call.args[0] for call in service.report_repository.add_photo.call_args_list]
    assert [saved.file_path for saved in added_photos] == ["reports/fix_before.jpg", "reports/fix_after.jpg"]
    assert all(isinstance(saved, ReportPhoto) for saved in added_photos)
    status_entry = service.report_repository.add_status_entry.call_args.args[0]
    assert isinstance(status_entry, ReportStatusHistory)
    assert status_entry.previous_status is None
    assert status_entry.new_status == ReportStatus.PENDING_APPROVAL
    assert status_entry.changed_by_id == reporter.id
    service.session.flush.assert_called_once()
    service.session.commit.assert_called_once()
    service.report_repository.get_by_id.assert_called_once_with(created_report.id)

@pytest.mark.parametrize("bad_category_id", ["abc", object()])
@pytest.mark.unit
def test_create_report_rejects_malformed_category_id(bad_category_id):
    service = make_service()

    with pytest.raises(ValidationError, match="valid active category"):
        service.create_report(user(), bad_category_id, "Title", "Description", 1.0, 2.0, [photo()])


@pytest.mark.parametrize(
    ("category_value", "title", "description", "latitude", "longitude", "photos", "message"),
    [
        (None, "Title", "Description", 1.0, 2.0, [photo()], "valid active category"),
        (category(is_active=False), "Title", "Description", 1.0, 2.0, [photo()], "valid active category"),
        (category(), "", "Description", 1.0, 2.0, [photo()], "Title and description"),
        (category(), "Title", None, 1.0, 2.0, [photo()], "Title and description"),
        (category(), "Title", "Description", None, 2.0, [photo()], "Latitude and longitude are required"),
        (category(), "Title", "Description", 1.0, None, [photo()], "Latitude and longitude are required"),
        (category(), "Title", "Description", "north", 2.0, [photo()], "valid numbers"),
        (category(), "Title", "Description", 1.0, "east", [photo()], "valid numbers"),
        (category(), "Title", "Description", 1.0, 2.0, [photo(None), None], "At least one photo"),
        (category(), "Title", "Description", 1.0, 2.0, [photo("1.jpg"), photo("2.jpg"), photo("3.jpg"), photo("4.jpg")], "at most 3"),
    ],
)

@pytest.mark.unit
def test_treate_report_validates(
    category_value,
    title,
    description,
    latitude,
    longitude,
    photos,
    message,
):
    service = make_service()
    service.category_repository.get_by_id.return_value = category_value

    with pytest.raises(ValidationError, match=message):
        service.create_report(user(), 10, title, description, latitude, longitude, photos)
    
    service.session.commit.assert_not_called()

@pytest.mark.unit
def test_follow_report_rejects_non_public_report():
    service = make_service()
    service.report_repository.get_by_id.return_value = report(status=ReportStatus.PENDING_APPROVAL)

    with pytest.raises(ValidationError, match="Only published reports"):
        service.follow_report(50, user(2))


def test_follow_report_returns_existing_followed_report_without_duplicate():
    service = make_service()
    public_report = report(status=ReportStatus.ASSIGNED)
    service.report_repository.get_by_id.return_value = public_report
    service.report_repository.get_follower.return_value = object()

    assert service.follow_report(public_report.id, user(2)) == public_report
    service.report_repository.add_follower.assert_not_called()
    service.session.commit.assert_not_called()


def test_follow_report_adds_follower_and_returns_reloaded_report():
    service = make_service()
    public_report = report(50, status=ReportStatus.ASSIGNED)
    reloaded_report = report(50, status=ReportStatus.ASSIGNED)
    service.report_repository.get_by_id.side_effect = [public_report, reloaded_report]
    service.report_repository.get_follower.return_value = None
    follower_user = user(22)

    result = service.follow_report(public_report.id, follower_user)

    assert result == reloaded_report
    added_follower = service.report_repository.add_follower.call_args.args[0]
    assert isinstance(added_follower, ReportFollower)
    assert added_follower.report_id == public_report.id
    assert added_follower.user_id == follower_user.id
    service.session.commit.assert_called_once()


def test_unfollow_report_removes_existing_follower_and_returns_reloaded_report():
    service = make_service()
    existing_follower = object()
    original_report = report(50)
    reloaded_report = report(50)
    service.report_repository.get_by_id.side_effect = [original_report, reloaded_report]
    service.report_repository.get_follower.return_value = existing_follower

    result = service.unfollow_report(50, user(22))

    assert result == reloaded_report
    service.report_repository.remove_follower.assert_called_once_with(existing_follower)
    service.session.commit.assert_called_once()


def test_unfollow_report_without_follower_only_returns_reloaded_report():
    service = make_service()
    original_report = report(50)
    reloaded_report = report(50)
    service.report_repository.get_by_id.side_effect = [original_report, reloaded_report]
    service.report_repository.get_follower.return_value = None

    assert service.unfollow_report(50, user(22)) == reloaded_report
    service.report_repository.remove_follower.assert_not_called()
    service.session.commit.assert_not_called()


def test_list_pending_reports_delegates_filter_values_to_repository():
    service = make_service()
    expected_reports = [report(status=ReportStatus.PENDING_APPROVAL)]
    service.report_repository.list_pending.return_value = expected_reports
    filters = {
        "category_id": 10,
        "date_from": datetime(2026, 1, 1),
        "date_to": datetime(2026, 1, 31),
        "ignored": "value",
    }

    assert service.list_pending_reports(filters) == expected_reports
    service.report_repository.list_pending.assert_called_once_with(
        category_id=10,
        date_from=filters["date_from"],
        date_to=filters["date_to"],
    )


def test_list_operator_reports_delegates_role_and_category():
    service = make_service()
    operator = user(5, Role.OPERATOR, category_id=10)
    expected_reports = [report(category_id=10)]
    service.report_repository.list_operator_reports.return_value = expected_reports

    assert service.list_operator_reports(operator) == expected_reports
    service.report_repository.list_operator_reports.assert_called_once_with(Role.OPERATOR, 10)


def test_assign_report_rejects_citizen_operator():
    service = make_service()

    with pytest.raises(AuthorizationError, match="Only operators or admins"):
        service.assign_report(50, user(1, Role.CITIZEN))


def test_assign_report_rejects_non_pending_report():
    service = make_service()
    assigned_report = report(status=ReportStatus.ASSIGNED)
    service.report_repository.get_by_id.return_value = assigned_report

    with pytest.raises(ValidationError, match="Only pending reports"):
        service.assign_report(assigned_report.id, user(2, Role.OPERATOR, category_id=10))


def test_assign_report_updates_status_history_notifies_and_returns_reloaded_report():
    service = make_service()
    pending_report = report(50, status=ReportStatus.PENDING_APPROVAL, category_id=10)
    pending_report.reporter = user(1)
    pending_report.followers = [follower(user(2)), follower(None)]
    reloaded_report = report(50, status=ReportStatus.ASSIGNED, category_id=10)
    service.report_repository.get_by_id.side_effect = [pending_report, reloaded_report]
    operator = user(9, Role.OPERATOR, category_id=10)

    result = service.assign_report(pending_report.id, operator)

    assert result == reloaded_report
    assert pending_report.status == ReportStatus.ASSIGNED
    status_entry = service.report_repository.add_status_entry.call_args.args[0]
    assert isinstance(status_entry, ReportStatusHistory)
    assert status_entry.previous_status == ReportStatus.PENDING_APPROVAL
    assert status_entry.new_status == ReportStatus.ASSIGNED
    assert status_entry.note == "Accepted for category 'Roads'."
    assert status_entry.changed_by_id == operator.id
    service.notification_service.notify_status_change.assert_called_once_with(
        recipients=[pending_report.reporter, pending_report.followers[0].user],
        report=pending_report,
        body="Report #50 has been assigned for handling in category 'Roads'.",
    )
    service.session.commit.assert_called_once()


def test_update_status_rejects_non_operator_roles_before_loading_report():
    service = make_service()

    with pytest.raises(AuthorizationError, match="Only operators and admins"):
        service.update_status(50, user(1, Role.CITIZEN), ReportStatus.ASSIGNED.value)

    service.report_repository.get_by_id.assert_not_called()


def test_update_status_rejects_invalid_status_value():
    service = make_service()
    pending_report = report(status=ReportStatus.PENDING_APPROVAL)
    service.report_repository.get_by_id.return_value = pending_report

    with pytest.raises(ValidationError, match="Invalid report status"):
        service.update_status(50, user(2, Role.OPERATOR, category_id=10), "bad-status")


def test_update_status_requires_rejection_reason():
    service = make_service()
    pending_report = report(status=ReportStatus.PENDING_APPROVAL)
    service.report_repository.get_by_id.return_value = pending_report

    with pytest.raises(ValidationError, match="Rejection reason"):
        service.update_status(50, user(2, Role.OPERATOR, category_id=10), ReportStatus.REJECTED.value)


def test_update_status_updates_report_history_notifies_and_returns_reloaded_report():
    service = make_service()
    assigned_report = report(50, status=ReportStatus.ASSIGNED, category_id=10)
    assigned_report.reporter = user(1)
    assigned_report.followers = [follower(user(2))]
    reloaded_report = report(50, status=ReportStatus.IN_PROGRESS, category_id=10)
    service.report_repository.get_by_id.side_effect = [assigned_report, reloaded_report]
    operator = user(9, Role.OPERATOR, category_id=10)

    result = service.update_status(
        report_id=assigned_report.id,
        operator=operator,
        next_status_value=ReportStatus.IN_PROGRESS.value,
        note="Work started.",
    )

    assert result == reloaded_report
    assert assigned_report.status == ReportStatus.IN_PROGRESS
    assert assigned_report.rejection_reason is None
    status_entry = service.report_repository.add_status_entry.call_args.args[0]
    assert isinstance(status_entry, ReportStatusHistory)
    assert status_entry.previous_status == ReportStatus.ASSIGNED
    assert status_entry.new_status == ReportStatus.IN_PROGRESS
    assert status_entry.note == "Work started."
    assert status_entry.changed_by_id == operator.id
    service.notification_service.notify_status_change.assert_called_once_with(
        recipients=[assigned_report.reporter, assigned_report.followers[0].user],
        report=assigned_report,
        body="Report #50 is now 'In Progress'.",
    )
    service.session.commit.assert_called_once()


def test_update_status_stores_rejection_reason_when_rejected():
    service = make_service()
    pending_report = report(50, status=ReportStatus.PENDING_APPROVAL, category_id=10)
    reloaded_report = report(50, status=ReportStatus.REJECTED, category_id=10)
    service.report_repository.get_by_id.side_effect = [pending_report, reloaded_report]

    result = service.update_status(
        report_id=50,
        operator=user(9, Role.ADMIN),
        next_status_value=ReportStatus.REJECTED.value,
        note="Duplicate report.",
    )

    assert result == reloaded_report
    assert pending_report.status == ReportStatus.REJECTED
    assert pending_report.rejection_reason == "Duplicate report."


def test_export_rows_serializes_public_reports():
    service = make_service()
    service.report_repository.list_reports.return_value = [
        report(10, ReportStatus.RESOLVED, category_id=3),
        report(11, ReportStatus.ASSIGNED, category_id=4),
    ]

    rows = service.export_rows(category_id=3, status=ReportStatus.RESOLVED, sort="asc")

    assert rows == [
        {
            "id": 10,
            "title": "BROKEN",
            "category": "Roads",
            "status": "Resolved",
            "created_at": "2026-01-02T03:04:05",
            "latitude": 20.0,
            "longitude": 20.0,
        },
        {
            "id": 11,
            "title": "BROKEN",
            "category": "Roads",
            "status": "Assigned",
            "created_at": "2026-01-02T03:04:05",
            "latitude": 20.0,
            "longitude": 20.0,
        },
    ]
    service.report_repository.list_reports.assert_called_once_with(
        public_only=True,
        category_id=3,
        status=ReportStatus.RESOLVED,
        date_from=None,
        date_to=None,
        sort="asc",
    )


def test_is_public_reflects_public_visible_statuses():
    assert ReportService.is_public(report(status=ReportStatus.ASSIGNED)) is True
    assert ReportService.is_public(report(status=ReportStatus.PENDING_APPROVAL)) is False


def test_recipients_returns_reporter_and_followers_without_none_values():
    reporter = user(1)
    follower_user = user(2)
    target_report = report()
    target_report.reporter = reporter
    target_report.followers = [follower(follower_user), follower(None)]

    assert ReportService._recipients(target_report) == [reporter, follower_user]


def test_ensure_operator_category_access_allows_admin_and_matching_operator():
    target_report = report(category_id=10)

    assert ReportService._ensure_operator_category_access(user(1, Role.ADMIN), target_report) is None
    assert ReportService._ensure_operator_category_access(user(2, Role.OPERATOR, 10), target_report) is None


def test_ensure_operator_category_access_rejects_invalid_role_and_category():
    target_report = report(category_id=10)

    with pytest.raises(AuthorizationError, match="Only operators and admins"):
        ReportService._ensure_operator_category_access(user(1, Role.CITIZEN), target_report)
    with pytest.raises(AuthorizationError, match="does not belong"):
        ReportService._ensure_operator_category_access(user(2, Role.OPERATOR, 99), target_report)