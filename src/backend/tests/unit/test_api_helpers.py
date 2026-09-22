from __future__ import annotations

import pytest

from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus
from participium.routes.api import _as_bool, _parse_report_status


@pytest.mark.unit
@pytest.mark.parametrize("value", [True, "1", "true", "yes", "on", " ON "])
def test_api_as_bool_returns_true_for_truthy_values(value):
    assert _as_bool(value) is True


@pytest.mark.unit
@pytest.mark.parametrize("value", [False, "0", "false", "no", "off", "", "anything"])
def test_api_as_bool_returns_false_for_non_truthy_values(value):
    assert _as_bool(value) is False


@pytest.mark.unit
def test_api_as_bool_returns_default_for_none():
    assert _as_bool(None) is False
    assert _as_bool(None, default=True) is True


@pytest.mark.unit
def test_parse_report_status_returns_none_for_empty_value():
    assert _parse_report_status(None) is None
    assert _parse_report_status("") is None


@pytest.mark.unit
def test_parse_report_status_returns_enum_for_valid_value():
    assert _parse_report_status("assigned") == ReportStatus.ASSIGNED


@pytest.mark.unit
def test_parse_report_status_raises_validation_error_for_invalid_value():
    with pytest.raises(ValidationError, match="Invalid report status filter"):
        _parse_report_status("bad-status")