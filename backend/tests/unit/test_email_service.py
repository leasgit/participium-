from __future__ import annotations

import pytest

from unittest.mock import Mock, patch

from participium.services.email_service import ConsoleEmailGateway, SmtpEmailGateway, build_email_gateway

# --- TESTS FOR CONSOLE GATEWAY ---

@pytest.mark.unit
def test_console_email_gateway_writes_file(tmp_path):
    """
    Tests that ConsoleGateway writes a correct text file
    """
    # Mock
    gateway = ConsoleEmailGateway(outbox_dir=tmp_path, sender="sys@test.com")

    # Act
    gateway.send(recipient="user@test.com", subject="Test", body="Test email")
    
    files = list(tmp_path.glob("*.txt"))
    content = files[0].read_text(encoding="utf-8")

    # Assert
    assert len(files) == 1

    assert "FROM: sys@test.com" in content
    assert "TO: user@test.com" in content
    assert "SUBJECT: Test" in content
    assert "Test email" in content

# --- TESTS FOR SMTP GATEWAY ---

@pytest.mark.unit
@patch("participium.services.email_service.smtplib.SMTP")
def test_smtp_email_gateway_with_auth_and_tls(mock_smtp_class):
    """
    Tests the SMTP send with TLS and credentials (mocking internet connection)
    """

    # Mocks
    mock_smtp_instance = Mock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    gateway = SmtpEmailGateway(
        host="smtp.test.com", port=587,
        username="user", password="pwd",
        sender="noreply@test.com", use_tls=True
    )

    # Calls
    gateway.send(recipient="user@test.com", subject="Test", body="Test email")

    # Assertions
    mock_smtp_class.assert_called_once_with("smtp.test.com", 587, timeout=10)
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with("user", "pwd")
    mock_smtp_instance.send_message.assert_called_once()

@pytest.mark.unit
@patch("participium.services.email_service.smtplib.SMTP")
def test_smtp_email_gateway_no_auth_no_tls(mock_smtp_class):
    """
    Tests the SMTP send without TLS and credentials
    """

    # Mocks
    mock_smtp_instance = Mock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    gateway = SmtpEmailGateway(
        host="localhost", port=25,
        username=None, password=None,
        sender="noreply@test.com", use_tls=False
    )

    # Calls
    gateway.send("user@test.com", "Test", "Test email")

    # Assertions
    mock_smtp_instance.starttls.assert_not_called()
    mock_smtp_instance.login.assert_not_called()
    mock_smtp_instance.send_message.assert_called_once()

# --- TESTS FOR BUILD EMAIL GATEWAY ---

@pytest.mark.unit
def test_build_email_gateway_smtp(tmp_path):
    """
    Tests that build_email_gateway return a SmtpGateway if configured
    """

    # Mocks
    settings = Mock(
        mail_backend="smtp",
        smtp_host="smtp.test.com",
        smtp_port=587,
        smtp_username="usr",
        smtp_password="pwd",
        mail_from="sys@test.com",
        smtp_use_tls=True
    )

    # Calls
    gateway = build_email_gateway(settings)

    # Assertions
    assert isinstance(gateway, SmtpEmailGateway)

def test_build_email_gateway_console(tmp_path):
    """
    Tests that build_email_gateway return ConsoleGateway if not smtp_host
    """

    # Mocks
    settings = Mock(
        mail_backend="console",
        smtp_host=None,
        mail_outbox_dir=tmp_path,
        mail_from="sys@test.com"
    )

    # Calls
    gateway = build_email_gateway(settings)

    # Assertions
    assert isinstance(gateway, ConsoleEmailGateway)