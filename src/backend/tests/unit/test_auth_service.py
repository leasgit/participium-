from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from participium.services.auth_service import AuthService
from participium.core.exceptions import AuthorizationError

def test_authenticate_logic_success(mock_user_repo):
    """Verifies authentication logic when password is correct"""
    service = AuthService(user_repository=mock_user_repo)
    mock_user = MagicMock(username="test_user", password_hash="hashed_pw", is_verified=True)
    mock_user_repo.find_by_identifier.return_value = mock_user

    with patch("participium.core.security.verify_password", return_value=True):
        result = service.authenticate("test_user", "password123")
        assert result.username == "test_user"

def test_authenticate_logic_failure(mock_user_repo):
    """Verifies that wrong passwords raise UnauthorizedError"""
    service = AuthService(user_repository=mock_user_repo)
    mock_user_repo.find_by_identifier.return_value = MagicMock()

    with patch("participium.core.security.verify_password", return_value=False):
        with pytest.raises(AuthorizationError):
            service.authenticate("test_user", "wrong_pass")