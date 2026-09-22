from __future__ import annotations

import pytest

from participium.database.seed import _ensure_demo_photo, seed_demo_data, seed_reference_data
from participium.models.category import Category
from participium.models.enums import Role
from participium.models.report import Report, ReportPhoto, ReportStatusHistory
from participium.models.user import User


@pytest.mark.integration
def test_seed_reference_data_creates_default_categories(db_session):
    seed_reference_data(db_session)

    categories = db_session.query(Category).all()

    assert len(categories) > 0
    assert all(category.is_active for category in categories)


@pytest.mark.integration
def test_seed_reference_data_is_idempotent(db_session):
    seed_reference_data(db_session)
    first_count = db_session.query(Category).count()

    seed_reference_data(db_session)
    second_count = db_session.query(Category).count()

    assert second_count == first_count


@pytest.mark.integration
def test_ensure_demo_photo_creates_file_when_media_root_provided(tmp_path):
    result = _ensure_demo_photo(tmp_path, "demo-report-photo.svg")

    created_file = tmp_path / "demo-report-photo.svg"

    assert result == "demo-report-photo.svg"
    assert created_file.exists()
    assert "Participium demo photo" in created_file.read_text(encoding="utf-8")


@pytest.mark.integration
def test_ensure_demo_photo_returns_filename_without_media_root():
    assert _ensure_demo_photo(None, "demo-report-photo.svg") == "demo-report-photo.svg"


@pytest.mark.integration
def test_seed_demo_data_creates_users_reports_photos_and_history(db_session, tmp_path):
    seed_reference_data(db_session)

    seed_demo_data(db_session, tmp_path)

    assert db_session.query(User).filter_by(email="citizen@example.com").first().role == Role.CITIZEN
    assert db_session.query(User).filter_by(email="operator@example.com").first().role == Role.OPERATOR
    assert db_session.query(User).filter_by(email="admin@example.com").first().role == Role.ADMIN

    assert db_session.query(Report).count() == 2
    assert db_session.query(ReportPhoto).count() == 2
    assert db_session.query(ReportStatusHistory).count() == 4
    assert (tmp_path / "demo-report-photo.svg").exists()


@pytest.mark.integration
def test_seed_demo_data_is_idempotent(db_session, tmp_path):
    seed_reference_data(db_session)
    seed_demo_data(db_session, tmp_path)

    first_users = db_session.query(User).count()
    first_reports = db_session.query(Report).count()
    first_photos = db_session.query(ReportPhoto).count()
    first_history = db_session.query(ReportStatusHistory).count()

    seed_demo_data(db_session, tmp_path)

    assert db_session.query(User).count() == first_users
    assert db_session.query(Report).count() == first_reports
    assert db_session.query(ReportPhoto).count() == first_photos
    assert db_session.query(ReportStatusHistory).count() == first_history