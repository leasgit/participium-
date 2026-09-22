from __future__ import annotations

from participium.core.status_flow import ensure_transition_allowed
from participium.models.enums import ReportStatus
from participium.core.exceptions import ValidationError

import pytest

@pytest.mark.parametrize(
    "current_status, next_status, expected_exception, oracle", 
    [
        (ReportStatus.PENDING_APPROVAL, ReportStatus.PENDING_APPROVAL, None, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED, None, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.REJECTED, None, True),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.IN_PROGRESS, ValidationError, None),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.SUSPENDED, ValidationError, None),
        (ReportStatus.PENDING_APPROVAL, ReportStatus.RESOLVED, ValidationError, None),
        (ReportStatus.ASSIGNED, ReportStatus.PENDING_APPROVAL, ValidationError, None),
        (ReportStatus.ASSIGNED, ReportStatus.ASSIGNED, None, True),
        (ReportStatus.ASSIGNED, ReportStatus.REJECTED, ValidationError, None),
        (ReportStatus.ASSIGNED, ReportStatus.IN_PROGRESS, None, True),
        (ReportStatus.ASSIGNED, ReportStatus.SUSPENDED, None, True),
        (ReportStatus.ASSIGNED, ReportStatus.RESOLVED, None, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.PENDING_APPROVAL, ValidationError, None),
        (ReportStatus.IN_PROGRESS, ReportStatus.ASSIGNED, ValidationError, None),
        (ReportStatus.IN_PROGRESS, ReportStatus.REJECTED, ValidationError, None),
        (ReportStatus.IN_PROGRESS, ReportStatus.IN_PROGRESS, None, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.SUSPENDED, None, True),
        (ReportStatus.IN_PROGRESS, ReportStatus.RESOLVED, None, True),
        (ReportStatus.SUSPENDED, ReportStatus.PENDING_APPROVAL, ValidationError, None),
        (ReportStatus.SUSPENDED, ReportStatus.ASSIGNED, ValidationError, None),
        (ReportStatus.SUSPENDED, ReportStatus.REJECTED, ValidationError, None),
        (ReportStatus.SUSPENDED, ReportStatus.IN_PROGRESS, None, True),
        (ReportStatus.SUSPENDED, ReportStatus.SUSPENDED, None, True),
        (ReportStatus.SUSPENDED, ReportStatus.RESOLVED, None, True),
        (ReportStatus.REJECTED, ReportStatus.PENDING_APPROVAL, ValidationError, None),
        (ReportStatus.REJECTED, ReportStatus.ASSIGNED, ValidationError, None),
        (ReportStatus.REJECTED, ReportStatus.REJECTED, None, True),
        (ReportStatus.REJECTED, ReportStatus.IN_PROGRESS, ValidationError, None),
        (ReportStatus.REJECTED, ReportStatus.SUSPENDED, ValidationError, None),
        (ReportStatus.REJECTED, ReportStatus.RESOLVED, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.PENDING_APPROVAL, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.ASSIGNED, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.REJECTED, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.IN_PROGRESS, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.SUSPENDED, ValidationError, None),
        (ReportStatus.RESOLVED, ReportStatus.RESOLVED, None, True),
    ]
)
def test_ensure_transition_allowed(current_status, next_status, expected_exception, oracle):
    if expected_exception : 
        with pytest.raises(expected_exception):
            ensure_transition_allowed(current_status, next_status)
    else: 
        assert ensure_transition_allowed(current_status, next_status) == oracle
