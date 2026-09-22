from __future__ import annotations
from datetime import datetime
import pytest
from participium.core.utils import parse_date

# Mark as blackbox for organization
pytestmark = pytest.mark.blackbox

def test_parse_date_valid():
    """TC-2.1: Parses valid ISO date string into datetime object"""
    result = parse_date("2026-04-25")
    assert isinstance(result, datetime)
    assert result.year == 2026
    assert result.month == 4
    assert result.day == 25

def test_parse_date_none():
    """TC-2.2: Returns None when input is None"""
    result = parse_date(None)
    assert result is None

def test_parse_date_invalid():
    """TC-2.3: Raises ValueError for non-date strings"""
    with pytest.raises(ValueError):
        parse_date("invalid_date")