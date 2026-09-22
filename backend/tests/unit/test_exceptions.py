from __future__ import annotations

import pytest

from participium.core.exceptions import (
    DomainError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
)


@pytest.mark.unit
def test_domain_error_uses_default_status_code():
    error = DomainError("Something went wrong")

    assert str(error) == "Something went wrong"
    assert error.status_code == 400


@pytest.mark.unit
def test_domain_error_allows_custom_status_code():
    error = DomainError("Custom error", status_code=499)

    assert str(error) == "Custom error"
    assert error.status_code == 499


@pytest.mark.unit
def test_validation_error_has_correct_status_code():
    error = ValidationError("Validation failed")

    assert str(error) == "Validation failed"
    assert error.status_code == 400
    assert isinstance(error, DomainError)


@pytest.mark.unit
def test_authentication_error_has_correct_status_code():
    error = AuthenticationError("Authentication failed")

    assert str(error) == "Authentication failed"
    assert error.status_code == 401
    assert isinstance(error, DomainError)


@pytest.mark.unit
def test_authorization_error_has_correct_status_code():
    error = AuthorizationError("Forbidden")

    assert str(error) == "Forbidden"
    assert error.status_code == 403
    assert isinstance(error, DomainError)


@pytest.mark.unit
def test_not_found_error_has_correct_status_code():
    error = NotFoundError("Resource not found")

    assert str(error) == "Resource not found"
    assert error.status_code == 404
    assert isinstance(error, DomainError)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("exception_class", "expected_status"),
    [
        (ValidationError, 400),
        (AuthenticationError, 401),
        (AuthorizationError, 403),
        (NotFoundError, 404),
    ],
)
def test_domain_exception_status_codes(exception_class, expected_status):
    error = exception_class("Failure")

    assert error.status_code == expected_status