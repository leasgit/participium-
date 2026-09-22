import pytest

from unittest.mock import Mock

from participium.controllers.admin_controller import AdminController
from participium.models.enums import Role

@pytest.fixture
def mocked_services():
    """
    Create and return mocks for services used by the Admin Controller
    """
    category_service = Mock()
    user_service = Mock()
    statistics_service = Mock()
    return category_service, user_service, statistics_service

@pytest.fixture
def admin_controller(mocked_services):
    """
    Initialize the Admin Controller with mocked services
    """
    category_service, user_service, statistics_service = mocked_services
    return AdminController(
        category_service=category_service,
        user_service=user_service,
        statistics_service=statistics_service
    )

# --- TESTS CATEGORY MANAGEMENT ---

@pytest.mark.unit
def test_list_categories(admin_controller, mocked_services):
    category_service, _, _ = mocked_services
    category_service.list_categories.return_value = ["cat1", "cat2"]

    # Test con active_only=True
    result = admin_controller.list_categories(active_only=True)
    category_service.list_categories.assert_called_once_with(active_only=True)
    assert result == ["cat1", "cat2"]

@pytest.mark.unit
def test_create_category(admin_controller, mocked_services):
    category_service, _, _ = mocked_services
    category_service.create_category.return_value = "new_cat"

    result = admin_controller.create_category("Security")
    category_service.create_category.assert_called_once_with("Security")
    assert result == "new_cat"

@pytest.mark.unit
def test_update_category(admin_controller, mocked_services):
    """
    Tests that the payload is unpacked correctly by the controller
    """
    category_service, _, _ = mocked_services
    category_service.update_category.return_value = "updated_cat"

    payload = {"name": "New Name", "is_active": False, "extra_field": "ignore_me"}
    
    result = admin_controller.update_category(category_id=5, payload=payload)
    
    category_service.update_category.assert_called_once_with(
        5,
        name="New Name",
        is_active=False
    )
    assert result == "updated_cat"

@pytest.mark.unit
def test_update_category_partial_payload(admin_controller, mocked_services):
    """Verifica il comportamento se il payload è incompleto (es. solo nome)."""
    category_service, _, _ = mocked_services
    payload = {"name": "New Name"}
    
    admin_controller.update_category(category_id=1, payload=payload)
    
    category_service.update_category.assert_called_once_with(
        1,
        name="New Name",
        is_active=None
    )

# --- TESTS USER MANAGEMENT ---

@pytest.mark.unit
def test_list_users(admin_controller, mocked_services):
    _, user_service, _ = mocked_services
    user_service.list_users.return_value = ["user1"]

    result = admin_controller.list_users()
    user_service.list_users.assert_called_once()
    assert result == ["user1"]

@pytest.mark.unit
def test_create_user(admin_controller, mocked_services):
    _, user_service, _ = mocked_services
    payload = {"username": "admin2", "role": Role.ADMIN}
    
    admin_controller.create_user(payload)
    user_service.create_user.assert_called_once_with(payload)

@pytest.mark.unit
def test_update_user(admin_controller, mocked_services):
    _, user_service, _ = mocked_services
    payload = {"role": Role.CITIZEN}
    
    admin_controller.update_user(user_id=42, payload=payload)
    user_service.update_user.assert_called_once_with(42, payload)

# --- TESTS STATISTICS MANAGEMENT ---

@pytest.mark.unit
def test_admin_statistics(admin_controller, mocked_services):
    _, _, statistics_service = mocked_services
    expected_stats = {"reports_by_status": {"Resolved": 10}}
    statistics_service.admin_statistics.return_value = expected_stats

    result = admin_controller.admin_statistics()
    
    statistics_service.admin_statistics.assert_called_once()
    assert result == expected_stats