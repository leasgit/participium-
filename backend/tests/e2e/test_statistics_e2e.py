from __future__ import annotations

import pytest

from participium.database.session import get_session
from participium.models.category import Category
from participium.models.enums import ReportStatus
from participium.models.report import Report
from datetime import datetime
from participium.models.enums import Role
from participium.models.user import User
from werkzeug.security import generate_password_hash

@pytest.mark.e2e
def test_public_statistics_endpoint_return_200(client):
    """
    Tests that the public endpoint returns aggregated data correctly
    """
    # Setup
    session = get_session()
    cat = Category(name="Roads", is_active=True)
    session.add(cat)
    session.commit()

    report = Report(
        title="Broken semaphore", description="...", category=cat,
        status=ReportStatus.RESOLVED, latitude=45.0, longitude=7.0,
        created_at=datetime(2026, 5, 1)
    )
    session.add(report)
    session.commit()

    # Call
    res = client.get("/api/v1/stats/public")
    data = res.get_json()

    # Assert
    assert res.status_code == 200
    assert "total_reports" in data
    assert data["total_reports"] == 1
    assert "reports_by_category" in data
    assert data["reports_by_category"]["Roads"] == 1

@pytest.mark.e2e
def test_admin_statistics_endpoint_forbidden_for_citizen(client):
    """
    Tests that a citizen can't access admin statistics
    """
    # Setup
    session = get_session()

    citizen = User(username="mario10",
        first_name="Mario",
        last_name="Rossi",
        email="mario@test.com",
        role=Role.CITIZEN,
        password_hash=generate_password_hash("pwd"),
        is_active=True,
        is_email_verified=True
    )
    session.add(citizen)
    session.commit()

    login_response = client.post("/api/v1/auth/login", json={
        "identifier":"mario10",
        "password": "pwd"
    })

    token = login_response.get_json().get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Call
    res = client.get("api/v1/admin/stats", headers=headers)

    # Assert
    assert res.status_code == 403