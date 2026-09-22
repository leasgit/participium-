from __future__ import annotations

import pytest


@pytest.mark.e2e
def test_health_endpoint_returns_ok(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


@pytest.mark.e2e
def test_reference_data_endpoint_returns_roles_and_statuses(client):
    response = client.get("/api/v1/meta/reference-data")

    data = response.get_json()

    assert response.status_code == 200
    assert "citizen" in data["roles"]
    assert "operator" in data["roles"]
    assert "admin" in data["roles"]
    assert "Pending Approval" in data["report_statuses"]
    assert "Assigned" in data["public_report_statuses"]


@pytest.mark.e2e
def test_unknown_api_route_returns_json_404(client):
    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Resource not found."}


@pytest.mark.e2e
def test_invalid_report_status_filter_returns_400(client):
    response = client.get("/api/v1/reports?status=bad-status")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid report status filter."}


@pytest.mark.e2e
def test_protected_route_requires_login(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
    assert "error" in response.get_json()