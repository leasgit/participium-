from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

import pytest

from participium.core.serialization import (
    _media_url,
    _serialize_party,
    _serialize_reporter,
    _viewer_follows_report,
    serialize_category,
    serialize_photo,
    serialize_user,
)
from participium.models.enums import Role


def user(user_id=1, role=Role.CITIZEN, category_id=None):
    return SimpleNamespace(
        id=user_id,
        username="john",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        role=role,
        category_id=category_id,
        category=None,
        is_active=True,
        is_email_verified=True,
        email_notifications_enabled=True,
        profile_picture_path="profiles/john.png",
        created_at=datetime(2026, 1, 1, 10, 30),
    )


def category():
    return SimpleNamespace(
        id=10,
        name="Roads",
        is_active=True,
        created_at=datetime(2026, 1, 2, 8, 15),
    )


def report(is_anonymous=True, reporter=None, reporter_id=1, category_id=10):
    return SimpleNamespace(
        is_anonymous=is_anonymous,
        reporter=reporter,
        reporter_id=reporter_id,
        category_id=category_id,
        followers=[],
    )


@pytest.mark.unit
def test_media_url_returns_none_for_empty_path():
    assert _media_url(None) is None
    assert _media_url("") is None


@pytest.mark.unit
def test_media_url_builds_static_upload_path():
    assert _media_url("reports/photo.jpg") == "/static/uploads/reports/photo.jpg"


@pytest.mark.unit
def test_serialize_category_returns_expected_dictionary():
    result = serialize_category(category())

    assert result == {
        "id": 10,
        "name": "Roads",
        "is_active": True,
        "created_at": "2026-01-02T08:15:00",
    }


@pytest.mark.unit
def test_serialize_user_includes_role_category_and_profile_picture_url():
    target_user = user()
    target_user.category = category()

    result = serialize_user(target_user)

    assert result["id"] == 1
    assert result["username"] == "john"
    assert result["email"] == "john@example.com"
    assert result["role"] == "citizen"
    assert result["category"]["name"] == "Roads"
    assert result["profile_picture_url"] == "/static/uploads/profiles/john.png"
    assert result["created_at"] == "2026-01-01T10:30:00"


@pytest.mark.unit
def test_serialize_party_returns_deleted_user_when_user_is_none():
    assert _serialize_party(None) == {
        "id": None,
        "display_name": "Deleted User",
        "role": None,
    }


@pytest.mark.unit
def test_serialize_party_uses_full_name_and_role():
    result = _serialize_party(user(role=Role.ADMIN))

    assert result == {
        "id": 1,
        "display_name": "John Doe",
        "role": "admin",
    }


@pytest.mark.unit
def test_serialize_reporter_hides_anonymous_reporter_from_public_viewer():
    reporter = user(user_id=5)
    target_report = report(is_anonymous=True, reporter=reporter, reporter_id=5)

    result = _serialize_reporter(target_report, viewer=None)

    assert result == {
        "display_name": "Anonymous Citizen",
        "id": None,
    }


@pytest.mark.unit
def test_serialize_reporter_shows_anonymous_reporter_to_admin():
    reporter = user(user_id=5)
    target_report = report(is_anonymous=True, reporter=reporter, reporter_id=5)

    result = _serialize_reporter(target_report, viewer=user(user_id=99, role=Role.ADMIN))

    assert result["id"] == 5
    assert result["display_name"] == "John Doe"
    assert result["role"] == "citizen"


@pytest.mark.unit
def test_serialize_reporter_shows_anonymous_reporter_to_matching_operator():
    reporter = user(user_id=5)
    target_report = report(
        is_anonymous=True,
        reporter=reporter,
        reporter_id=5,
        category_id=10,
    )

    result = _serialize_reporter(
        target_report,
        viewer=user(user_id=99, role=Role.OPERATOR, category_id=10),
    )

    assert result["id"] == 5


@pytest.mark.unit
def test_serialize_reporter_hides_anonymous_reporter_from_wrong_operator_category():
    reporter = user(user_id=5)
    target_report = report(
        is_anonymous=True,
        reporter=reporter,
        reporter_id=5,
        category_id=10,
    )

    result = _serialize_reporter(
        target_report,
        viewer=user(user_id=99, role=Role.OPERATOR, category_id=22),
    )

    assert result == {
        "display_name": "Anonymous Citizen",
        "id": None,
    }


@pytest.mark.unit
def test_viewer_follows_report_returns_true_when_viewer_is_follower():
    target_report = report()
    target_report.followers = [SimpleNamespace(user_id=2), SimpleNamespace(user_id=3)]

    assert _viewer_follows_report(target_report, user(user_id=3)) is True


@pytest.mark.unit
def test_viewer_follows_report_returns_false_without_viewer_or_match():
    target_report = report()
    target_report.followers = [SimpleNamespace(user_id=2)]

    assert _viewer_follows_report(target_report, None) is False
    assert _viewer_follows_report(target_report, user(user_id=3)) is False


@pytest.mark.unit
def test_serialize_photo_builds_photo_dto_with_media_url():
    photo = SimpleNamespace(
        id=7,
        file_path="reports/photo.jpg",
        original_filename="photo.jpg",
        content_type="image/jpeg",
    )

    result = serialize_photo(photo)

    assert result == {
        "id": 7,
        "file_path": "reports/photo.jpg",
        "url": "/static/uploads/reports/photo.jpg",
        "original_filename": "photo.jpg",
        "content_type": "image/jpeg",
    }