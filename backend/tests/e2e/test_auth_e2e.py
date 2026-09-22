import pytest

def test_e2e_registration_and_login(client):
    """Exercises the full stack from Route to DB for registration"""
    # 1. Register a new user
    reg_data = {
        "username": "new_citizen",
        "email": "new@example.com",
        "password": "SecurePassword123!",
        "first_name": "New",
        "last_name": "Citizen"
    }
    response = client.post("/api/auth/register", json=reg_data)
    assert response.status_code == 201

    # 2. Try to login with created credentials
    login_data = {"identifier": "new_citizen", "password": "SecurePassword123!"}
    login_res = client.post("/api/auth/login", json=login_data)
    assert login_res.status_code == 200
    assert "access_token" in login_res.get_json()