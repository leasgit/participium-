from __future__ import annotations

from unittest.mock import Mock

import pytest

from participium.repositories import user_repository
from participium.services.user_service import UserService
from participium.models.user import User
from participium.core.exceptions import ValidationError

pytestmark = pytest.mark.whitebox

# Structural tests for UserService.update_user belong here.
# The current runnable smoke check is kept in test_wb_task06_smoke.py.

# --- FIXTURES ---

def _user(*, id: int = 102, username: str = "luca.verdi", email: str = "luca.verdi@test.com") -> User:
    return User(
        id=id,
        username=username,
        first_name="Luca",
        last_name="Verdi",
        email=email,
        password_hash="HASH",
        role="USER",
        is_active=True,
        email_notifications_enabled=True,
    )

@pytest.fixture
def user_service_bundle() -> dict[str, object]:
    session = Mock()
    user_repository = Mock()
    service = UserService(session=session, user_repository=user_repository)

    service.get_user = Mock()
    service._parse_role = Mock(return_value="OPERATOR")
    service._resolve_operator_category = Mock()

    return {
        "service": service,
        "session": session,
        "user_repository": user_repository
    }

@pytest.fixture
def baseline_case(user_service_bundle: dict[str, object]) -> dict[str, object]:
    """TC-PC-5.1: Base case with existing user and empty payload."""
    user = _user()
    user_service_bundle["service"].get_user.return_value = user
    user_service_bundle["user"] = user
    return user_service_bundle

@pytest.fixture
def identity_update_case(user_service_bundle: dict[str, object]) -> dict[str, object]:
    """TC-PC-5.2 & TC-PC-5.5: Cases updating user fields with old value"""
    user = _user(username="old.username", email="old.email@test.com")
    user_service_bundle["service"].get_user.return_value = user
    user_service_bundle["user"] = user

    user_service_bundle["user_repository"].get_by_username.return_value = None
    user_service_bundle["user_repository"].get_by_email.return_value = None
    return user_service_bundle

@pytest.fixture
def collision_free_case(baseline_case: dict[str, object]) -> dict[str, object]:
    """TC-NC-5.3 & TC-PC-5.3 & TC-PC-5.6 & TC-PC-5.8 & TC-PC-5.9 & TC-PC-5.10 & TC-PC-5.11 & TC-PC-5.12 & TC-PC-5.13: Update with no collision cases"""
    baseline_case["user_repository"].get_by_username.return_value = None
    baseline_case["user_repository"].get_by_email.return_value = None

    category_mock = Mock()
    category_mock.id = 5
    baseline_case["service"]._resolve_operator_category.return_value = category_mock

    return baseline_case

@pytest.fixture
def collision_case(baseline_case: dict[str, object]) -> dict[str, object]:
    """TC-PC-5.4 & TC-PC-5.7: Username and email collision cases."""
    baseline_case["user_repository"].get_by_username.return_value = _user(id=999, username="luca.bianchi")
    baseline_case["user_repository"].get_by_email.return_value = _user(id=999, email="existing.email@test.com")
    return baseline_case

# --- TEST CASES ---

# TC-PC-5.1
def test_update_user_with_empty_payload(baseline_case: dict[str, object]) -> None:
    service = baseline_case["service"]
    user = baseline_case["user"]

    payload = {}

    result = service.update_user(user_id=102, payload=payload)

    assert result == user
    service.session.commit.assert_called_once()

# TC-PC-5.2
def test_update_user_with_same_username_does_not_trigger_validation(identity_update_case: dict[str, object]) -> None:
    service = identity_update_case["service"]
    user = identity_update_case["user"]
    user_repository = identity_update_case["user_repository"]

    payload = {"username": user.username}

    service.update_user(user_id=102, payload=payload)

    user_repository.get_by_username.assert_not_called()
    service.session.commit.assert_called_once()


# TC-PC-5.3
def test_update_user_with_new_valid_username_updates_successfully(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    new_username = "valid.username"
    payload = {"username": new_username}

    service.update_user(user_id=102, payload=payload)

    user_repository.get_by_username.assert_called_once_with(new_username)
    assert user.username == new_username
    service.session.commit.assert_called_once()

# TC-PC-5.4
def test_update_user_raises_error_on_username_collision(collision_case: dict[str, object]) -> None:
    service = collision_case["service"]

    payload = {"username": "luca.bianchi"}

    with pytest.raises(ValidationError, match="Username already in use."):
        service.update_user(user_id=102, payload=payload)

    service.session.commit.assert_not_called()

# TC-PC-5.5
def test_update_user_with_same_email_does_not_trigger_validation(identity_update_case: dict[str, object]) -> None:
    service = identity_update_case["service"]
    user = identity_update_case["user"]
    user_repository = identity_update_case["user_repository"]

    payload = {"email": user.email}

    service.update_user(user_id=102, payload=payload)

    user_repository.get_by_email.assert_not_called()
    service.session.commit.assert_called_once()

# TC-PC-5.6
def test_update_user_with_new_valid_email_updates_successfully(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    new_email = "valid.email@test.com"
    payload = {"email": new_email}

    service.update_user(user_id=102, payload=payload)

    user_repository.get_by_email.assert_called_once_with(new_email)
    assert user.email == new_email
    service.session.commit.assert_called_once()

# TC-PC-5.7
def test_update_user_raises_error_on_email_collision(collision_case: dict[str, object]) -> None:
    service = collision_case["service"]

    payload = {"email": "existing.email@test.com"}

    with pytest.raises(ValidationError, match="Email already in use."):
        service.update_user(user_id=102, payload=payload)

    service.session.commit.assert_not_called()

# TC-PC-5.8
def test_update_user_strips_strings_in_payload(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    payload = {"first_name": " Mario "}

    service.update_user(user_id=102, payload=payload)

    assert user.first_name == "Mario"
    service.session.commit.assert_called_once()

# TC-PC-5.9
def test_update_user_handles_non_string_values_in_loop(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]
    
    payload = {"first_name": 12345}

    service.update_user(user_id=102, payload=payload)

    assert user.first_name == 12345
    service.session.commit.assert_called_once()

# TC-PC-5.10
def test_update_user_category_via_only_role(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    new_role = "OPERATOR"
    payload = {"role": new_role}

    service.update_user(user_id=102, payload=payload)

    service._resolve_operator_category.assert_called_once_with(new_role, user.category_id)
    service.session.commit.assert_called_once()

# TC-PC-5.11
def test_update_category_via_only_id(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    new_category_id = 10
    payload = {"category_id": new_category_id}

    service.update_user(user_id=102, payload=payload)

    service._resolve_operator_category.assert_called_once_with(user.role, new_category_id)
    service.session.commit.assert_called_once()

# TC-PC-5.12
def test_update_user_activeness_updates_successfully(collision_free_case: dict[str, object]) -> None:
    service = baseline_case["service"]
    user = baseline_case["user"]

    payload = {"is_active": True}

    service.update_user(user_id=102, payload=payload)

    assert user.is_active is True
    service.session.commit.assert_called_once()

# TC-PC-5.13
def test_update_user_email_notifications_updates_successfully(collision_free_case: dict[str, object]) -> None:
    service = baseline_case["service"]
    user = baseline_case["user"]

    payload = {"email_notifications_enabled": True}

    service.update_user(user_id=102, payload=payload)

    assert user.email_notifications_enabled is True
    service.session.commit.assert_called_once()

# TC-NC-5.3
def test_update_user_full_path_updates_all_fields(collision_free_case: dict[str, object]) -> None:
    service = collision_free_case["service"]
    user = collision_free_case["user"]

    payload = {
        "username": "valid.username",
        "email": "valid.email@test.com",
        "first_name": "Mario",
        "role": "OPERATOR",
        "category_id": 5,
        "is_active": False,
        "email_notifications_enabled": True
    }

    service.update_user(user_id=102, payload=payload)

    assert user.username == "valid.username"
    assert user.email == "valid.email@test.com"
    assert user.role == "OPERATOR"
    assert user.category_id == 5
    assert user.is_active is False
    assert user.email_notifications_enabled is True
    service.session.commit.assert_called_once()
