from __future__ import annotations
from participium.models.report import Report, ReportFollower, ReportPhoto, ReportStatusHistory
from participium.models.enums import ReportStatus, Role
import pytest
from unittest.mock import Mock

from participium.repositories.report_repository import ReportRepository

from datetime import datetime

@pytest.fixture
def session():
    return Mock()

@pytest.fixture
def repository(session):
    return ReportRepository(session)

class UniqueScalarResult:
    def __init__(self, items):
        self.items = items
        self.unique_called = False

    def unique(self):
        self.unique_called = True
        return self

    def __iter__(self):
        return iter(self.items)


def compiled_sql(statement) -> str:
    return str(statement.compile(compile_kwargs={"literal_binds": True}))


@pytest.mark.unit
@pytest.mark.parametrize(
    ("method_name", "model_class"),
    [
        ("add", Report),
        ("add_photo", ReportPhoto),
        ("add_status_entry", ReportStatusHistory),
        ("add_follower", ReportFollower)
    ]
)

def test_add_methods_store_and_return_model(repository, session, method_name, model_class):
    model = Mock(spec=model_class)

    result = getattr(repository, method_name)(model)

    assert result is model
    session.add.assert_called_once_with(model)

@pytest.mark.unit
def test_get_follower_queries_by_report_and_user(repository, session):
    follower = Mock(spec=ReportFollower)
    session.scalar.return_value = follower

    result = repository.get_follower(report_id=10, user_id=20)

    assert result is follower
    sql = compiled_sql(session.scalar.call_args.args[0])
    assert "report_followers.report_id = 10" in sql
    assert "report_followers.user_id = 20" in sql

@pytest.mark.unit
def test_remove_follower_deletes_model(repository, session):
    follower = Mock(spec=ReportFollower)

    repository.remove_follower(follower)

    session.delete.assert_called_once_with(follower)

@pytest.mark.unit
def test_get_by_id_queries_report_with_detail_options(repository, session):
    report = Mock(spec=Report)
    session.scalar.return_value = report

    result = repository.get_by_id(report_id=7)

    assert result is report
    sql = compiled_sql(session.scalar.call_args.args[0])
    assert "reports.id = 7" in sql


@pytest.mark.unit
def test_list_reports_without_filters_uses_descending_order(repository, session):
    reports = [Mock(spec=Report)]
    scalar_result = UniqueScalarResult(reports)
    session.scalars.return_value = scalar_result

    result = repository.list_reports()

    assert result == reports
    assert scalar_result.unique_called is True
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "WHERE" not in sql
    assert "ORDER BY reports.created_at DESC" in sql


@pytest.mark.unit
def test_list_reports_applies_all_filters_and_ascending_order(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)
    date_from = datetime(2026, 5, 1)
    date_to = datetime(2026, 5, 8)

    result = repository.list_reports(
        public_only=True,
        category_id=3,
        status=ReportStatus.RESOLVED,
        date_from=date_from,
        date_to=date_to,
        sort="asc",
    )

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.status IN" in sql
    assert "reports.category_id = 3" in sql
    assert "reports.status = 'RESOLVED'" in sql
    assert "reports.created_at >= '2026-05-01 00:00:00'" in sql
    assert "reports.created_at <= '2026-05-08 00:00:00'" in sql
    assert "ORDER BY reports.created_at ASC" in sql


@pytest.mark.unit
def test_list_user_reports_filters_by_reporter(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)

    result = repository.list_user_reports(user_id=42)

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.reporter_id = 42" in sql
    assert "ORDER BY reports.created_at DESC" in sql

def where_clause(sql: str) -> str:
    if " WHERE " not in sql:
        return ""
    return sql.split(" WHERE ", 1)[1].split(" ORDER BY ", 1)[0]

@pytest.mark.unit
def test_list_pending_without_optional_filters(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)

    result = repository.list_pending()

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.status = 'PENDING_APPROVAL'" in sql
    assert "reports.category_id" not in where_clause(sql)
    assert "ORDER BY reports.created_at ASC" in sql


@pytest.mark.unit
def test_list_pending_applies_optional_filters(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)
    date_from = datetime(2026, 5, 1)
    date_to = datetime(2026, 5, 8)

    result = repository.list_pending(category_id=2, date_from=date_from, date_to=date_to)

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.category_id = 2" in sql
    assert "reports.created_at >= '2026-05-01 00:00:00'" in sql
    assert "reports.created_at <= '2026-05-08 00:00:00'" in sql


@pytest.mark.unit
def test_list_for_category_without_category(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)

    result = repository.list_for_category(None)

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.status != 'PENDING_APPROVAL'" in sql
    assert "reports.category_id" not in where_clause(sql)
    assert "ORDER BY reports.updated_at DESC" in sql


@pytest.mark.unit
def test_list_for_category_applies_category_filter(repository, session):
    reports = [Mock(spec=Report)]
    session.scalars.return_value = UniqueScalarResult(reports)

    result = repository.list_for_category(category_id=5)

    assert result == reports
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "reports.category_id = 5" in sql


@pytest.mark.unit
def test_list_operator_reports_scopes_operator_to_category(repository):
    repository.list_for_category = Mock(return_value=["operator reports"])

    result = repository.list_operator_reports(Role.OPERATOR, category_id=9)

    assert result == ["operator reports"]
    repository.list_for_category.assert_called_once_with(9)


@pytest.mark.unit
def test_list_operator_reports_admin_can_see_all_categories(repository):
    repository.list_for_category = Mock(return_value=["admin reports"])

    result = repository.list_operator_reports(Role.ADMIN, category_id=9)

    assert result == ["admin reports"]
    repository.list_for_category.assert_called_once_with(None)


@pytest.mark.unit
def test_list_followers_returns_scalar_results(repository, session):
    followers = [Mock(spec=ReportFollower), Mock(spec=ReportFollower)]
    session.scalars.return_value = followers
    
    result = repository.list_followers(report_id=8)

    assert result == followers
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "report_followers.report_id = 8" in sql


@pytest.mark.unit
def test_list_all_delegates_to_list_reports(repository):
    repository.list_reports = Mock(return_value=["report"])

    result = repository.list_all()

    assert result == ["report"]
    repository.list_reports.assert_called_once_with(public_only=False)