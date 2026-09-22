from __future__ import annotations

from participium.services.report_service import ReportService
import io
import pytest
from werkzeug.datastructures import FileStorage
from participium.core.exceptions import ValidationError
from participium.models.user import User
from participium.models.report import Report

VALID_USER = User(
    id=1,
    username="bruno.centrella",
    first_name="Bruno",
    last_name="Centrella",
    email="bruno.centrella@example.com",
    password_hash="HASHED_PASSWORD_1",
    is_active=True,
    is_email_verified=True,
)

ACTIVE_CATEGORY_ID_3 = 3
ACTIVE_CATEGORY_ID_2 = 2
ACTIVE_CATEGORY_ID_1 = 1
ACTIVE_CATEGORY_ID_4 = 4
INACTIVE_CATEGORY_ID = 101


def make_photo(filename="photo.jpg", content_type="image/jpeg"):
    return FileStorage(
        stream=io.BytesIO(b"fake image content"),
        filename=filename,
        content_type=content_type,
    )

@pytest.fixture
def seed_create_report_data() -> None:
    # Populate the system with the data needed by
    # `ReportService.create_report`.
    #
    # Suggested dataset:
    # - `VALID_USER` as a registered citizen
    # - Categories with id=1, 2, 3, 4 all with is_active=True
    # - A category with id=`INACTIVE_CATEGORY_ID` (101) and is_active=False
    pass


@pytest.mark.skip(reason="Disabled.")
def test_create_report_success(seed_create_report_data: None) -> None:
    report_service = ReportService()
    report = report_service.create_report(
        reporter=VALID_USER,
        category_id=3,
        title="Broken streetlight",
        description="Streetlight on Via Moretta has been broken for 4 days",
        latitude=45.0680,
        longitude=7.6531,
        photos=[make_photo("lamp.jpg")],
        is_anonymous=False,
    )
    assert isinstance(report, Report)
    assert report.title == "Broken streetlight"
    assert report.is_anonymous is False


@pytest.mark.skip(reason="Disabled.")
def test_create_report_anonymous(seed_create_report_data: None) -> None:
    report_service = ReportService()
    report = report_service.create_report(
        reporter=VALID_USER,
        category_id=3,
        title="Broken streetlight",
        description="Streetlight on Via Moretta has been broken for 4 days",
        latitude=45.0680,
        longitude=7.6531,
        photos=[make_photo("lamp.jpg")],
        is_anonymous=True,
    )
    assert isinstance(report, Report)
    assert report.is_anonymous is True


@pytest.mark.skip(reason="Disabled.")
def test_create_report_three_photos(seed_create_report_data: None) -> None:
    report_service = ReportService()
    report = report_service.create_report(
        reporter=VALID_USER,
        category_id=3,
        title="Broken streetlight",
        description="Streetlight on Via Moretta has been broken for 4 days",
        latitude=45.0680,
        longitude=7.6531,
        photos=[make_photo("lamp1.jpg"), make_photo("lamp2.jpg"), make_photo("lamp3.jpg")],
        is_anonymous=False,
    )
    assert isinstance(report, Report)
    assert len(report.photos) == 3


@pytest.mark.skip(reason="Disabled.")
def test_create_report_string_coordinates(seed_create_report_data: None) -> None:
    report_service = ReportService()
    report = report_service.create_report(
        reporter=VALID_USER,
        category_id=3,
        title="Broken streetlight",
        description="Streetlight on Via Moretta has been broken for 4 days",
        latitude="45.0680",
        longitude="7.6531",
        photos=[make_photo("lamp.jpg")],
        is_anonymous=False,
    )
    assert isinstance(report, Report)
    assert report.latitude == 45.0680
    assert report.longitude == 7.6531


@pytest.mark.skip(reason="Disabled.")
def test_create_report_missing_category(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=None,
            title="Pothole",
            description="Large pothole on Via Roma",
            latitude=45.0653,
            longitude=7.6808,
            photos=[make_photo("hole.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_malformed_category(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id="road damage",
            title="Pothole",
            description="Large pothole on Via Roma",
            latitude=45.0653,
            longitude=7.6808,
            photos=[make_photo("hole.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_inactive_category(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=101,
            title="Pothole",
            description="Large pothole on Via Roma",
            latitude=45.0653,
            longitude=7.6808,
            photos=[make_photo("hole.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_missing_title(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=2,
            title=None,
            description="Large pothole on Via Roma",
            latitude=45.0653,
            longitude=7.6808,
            photos=[make_photo("hole.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_missing_description(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=2,
            title="Pothole",
            description=None,
            latitude=45.0653,
            longitude=7.6808,
            photos=[make_photo("hole.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_missing_latitude(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=1,
            title="Damaged road sign",
            description="Stop sign knocked over",
            latitude=None,
            longitude=7.6808,
            photos=[make_photo("sign.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_missing_longitude(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=1,
            title="Damaged road sign",
            description="Stop sign knocked over",
            latitude=45.0653,
            longitude=None,
            photos=[make_photo("sign.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_invalid_latitude(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=1,
            title="Damaged road sign",
            description="Stop sign knocked over",
            latitude="south",
            longitude=7.6808,
            photos=[make_photo("sign.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_invalid_longitude(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=1,
            title="Damaged road sign",
            description="Stop sign knocked over",
            latitude=45.0653,
            longitude="west",
            photos=[make_photo("sign.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_no_photos(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=4,
            title="Broken bench",
            description="Completely broken bench in Parco del Valentino",
            latitude=45.0558,
            longitude=7.6883,
            photos=[],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_too_many_photos(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=4,
            title="Broken bench",
            description="Completely broken bench in Parco del Valentino",
            latitude=45.0558,
            longitude=7.6883,
            photos=[make_photo("bench1.jpg"), make_photo("bench2.jpg"), make_photo("bench3.jpg"), make_photo("bench4.jpg")],
            is_anonymous=False,
        )


@pytest.mark.skip(reason="Disabled.")
def test_create_report_photo_no_filename(seed_create_report_data: None) -> None:
    report_service = ReportService()
    with pytest.raises(ValidationError):
        report_service.create_report(
            reporter=VALID_USER,
            category_id=4,
            title="Broken bench",
            description="Completely broken bench in Parco del Valentino",
            latitude=45.0558,
            longitude=7.6883,
            photos=[make_photo(filename="")],
            is_anonymous=False,
        )