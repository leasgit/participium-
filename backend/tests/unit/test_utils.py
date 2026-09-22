from __future__ import annotations

from datetime import datetime

import pytest

from participium.core.utils import build_csv, parse_date, utcnow


@pytest.mark.unit
def test_utcnow_returns_datetime():
    result = utcnow()

    assert isinstance(result, datetime)


@pytest.mark.unit
def test_parse_date_returns_none_for_empty_values():
    assert parse_date(None) is None
    assert parse_date("") is None


@pytest.mark.unit
def test_parse_date_parses_iso_datetime_string():
    result = parse_date("2026-01-02T03:04:05")

    assert result == datetime(2026, 1, 2, 3, 4, 5)


@pytest.mark.unit
def test_parse_date_raises_value_error_for_invalid_string():
    with pytest.raises(ValueError):
        parse_date("not-a-date")


@pytest.mark.unit
def test_build_csv_writes_header_and_rows():
    rows = [
        {"id": 1, "name": "Roads"},
        {"id": 2, "name": "Parks"},
    ]

    result = build_csv(rows, ["id", "name"])

    assert result == "id,name\r\n1,Roads\r\n2,Parks\r\n"


@pytest.mark.unit
def test_build_csv_writes_only_header_when_rows_empty():
    result = build_csv([], ["id", "name"])

    assert result == "id,name\r\n"