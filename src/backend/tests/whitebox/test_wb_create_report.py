from __future__ import annotations
from unittest.mock import MagicMock, patch
import pytest

from participium.services.report_service import ReportService

pytestmark = pytest.mark.whitebox

def test_wb_create_report_t1(report_service):
    # Path: N1 -> N2 -> N8 -> N9
    with pytest.raises(ValueError):
        report_service.create_report(report_data=None, author_id=123)

def test_wb_create_report_t2(report_service):
    # Path: N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N9
    report_data = MagicMock(photos=[])
    
    with patch("participium.services.geocoding_service.GeocodingService.get_coords") as mock_geo:
        mock_geo.return_value = (45.0703, 7.6869)
        result = report_service.create_report(report_data=report_data, author_id=123)
        
        assert result is not None
        report_service.report_repository.save.assert_called_once()
        assert len(result.photos) == 0

def test_wb_create_report_t3(report_service):
    # Path: N1 -> N2 -> N3 -> N4 -> N5 -> N6 -> N7 -> N9
    report_data = MagicMock(photos=[MagicMock(), MagicMock(), MagicMock()])
    
    with patch("participium.services.geocoding_service.GeocodingService.get_coords") as mock_geo:
        mock_geo.return_value = (45.0703, 7.6869)
        result = report_service.create_report(report_data=report_data, author_id=123)
        
        assert result is not None
        report_service.report_repository.save.assert_called_once()
        assert len(result.photos) == 3

def test_wb_create_report_a4_null(report_service):
    # Path: N1 -> N2 -> N8 -> N9
    report_data = MagicMock(photos=[])
    with pytest.raises(ValueError):
        report_service.create_report(report_data=report_data, author_id=None)