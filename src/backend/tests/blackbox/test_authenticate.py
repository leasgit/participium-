from __future__ import annotations
import pytest
from backend.participium.core.exceptions import AuthorizationError, NotFoundError
from participium.services.auth_service import AuthService

# Mark as blackbox for organization
pytestmark = pytest.mark.blackbox

def test_authenticate_success():
    """TC-1.1: Returns User object when credentials are valid"""
    # Assumption: A verified user with identifier 'example_citizen' and password 'Pass123!' exists.
    auth_service = AuthService()
    user = auth_service.authenticate(identifier="example_citizen", password="Pass123!")
    
    assert user is not None
    assert user.username == "example_citizen"
    assert user.is_verified is True

def test_authenticate_wrong_password():
    """TC-1.2: Raises UnauthorizedError for incorrect password"""
    auth_service = AuthService()
    with pytest.raises(AuthorizationError):
        auth_service.authenticate(identifier="example_citizen", password="wrong_pass")

def test_authenticate_user_not_found():
    """TC-1.3: Raises NotFoundError for unknown identifier"""
    auth_service = AuthService()
    with pytest.raises(NotFoundError):
        auth_service.authenticate(identifier="unknown_user", password="any_pass")