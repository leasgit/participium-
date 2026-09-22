from __future__ import annotations

from pathlib import Path

import pytest

from participium.config.settings import Settings, _as_bool


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    ["1", "true", "TRUE", "yes", "on", " On "],
)
def test_as_bool_returns_true_for_truthy_values(value):
    assert _as_bool(value) is True


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    ["0", "false", "no", "off", "anything", ""],
)
def test_as_bool_returns_false_for_non_truthy_values(value):
    assert _as_bool(value) is False


@pytest.mark.unit
def test_as_bool_returns_default_when_value_is_none():
    assert _as_bool(None) is False
    assert _as_bool(None, default=True) is True


@pytest.mark.unit
def test_settings_from_env_uses_default_values(monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "change-me")
    monkeypatch.setenv("MEDIA_ROOT", str(tmp_path / "uploads"))
    monkeypatch.setenv("MAIL_OUTBOX_DIR", str(tmp_path / "outbox"))

    settings = Settings.from_env()

    assert settings.app_name == "Participium"
    assert settings.secret_key == "change-me"
    assert settings.debug is True
    assert settings.frontend_origin == "http://localhost:5173"
    assert settings.host == "0.0.0.0"
    assert settings.port == 5050
    assert settings.auto_init_db is True
    assert settings.bootstrap_reference_data is True
    assert settings.bootstrap_demo_data is True
    assert settings.mail_backend == "console"
    assert settings.mail_from == "noreply@participium.local"
    assert settings.smtp_host is None
    assert settings.smtp_port == 587
    assert settings.smtp_username is None
    assert settings.smtp_password is None
    assert settings.smtp_use_tls is True
    assert settings.expose_verification_links is True
    assert settings.max_content_length == 16 * 1024 * 1024
    assert settings.media_root == tmp_path / "uploads"
    assert settings.mail_outbox_dir == tmp_path / "outbox"
    assert settings.media_root.exists()
    assert settings.mail_outbox_dir.exists()
    assert isinstance(settings.instance_path, Path)


@pytest.mark.unit
def test_settings_from_env_reads_environment_overrides(monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("FRONTEND_ORIGIN", "https://example.com")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("PORT", "8080")
    monkeypatch.setenv("AUTO_INIT_DB", "false")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "no")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "0")
    monkeypatch.setenv("MAIL_BACKEND", "smtp")
    monkeypatch.setenv("MAIL_FROM", "test@example.com")
    monkeypatch.setenv("MAIL_OUTBOX_DIR", str(tmp_path / "mail"))
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "2525")
    monkeypatch.setenv("SMTP_USERNAME", "smtp-user")
    monkeypatch.setenv("SMTP_PASSWORD", "smtp-pass")
    monkeypatch.setenv("SMTP_USE_TLS", "off")
    monkeypatch.setenv("EXPOSE_VERIFICATION_LINKS", "false")
    monkeypatch.setenv("MEDIA_ROOT", str(tmp_path / "media"))
    monkeypatch.setenv("MAX_CONTENT_LENGTH", "12345")

    settings = Settings.from_env()

    assert settings.secret_key == "test-secret"
    assert settings.debug is False
    assert settings.frontend_origin == "https://example.com"
    assert settings.host == "127.0.0.1"
    assert settings.port == 8080
    assert settings.auto_init_db is False
    assert settings.bootstrap_reference_data is False
    assert settings.bootstrap_demo_data is False
    assert settings.mail_backend == "smtp"
    assert settings.mail_from == "test@example.com"
    assert settings.mail_outbox_dir == tmp_path / "mail"
    assert settings.smtp_host == "smtp.example.com"
    assert settings.smtp_port == 2525
    assert settings.smtp_username == "smtp-user"
    assert settings.smtp_password == "smtp-pass"
    assert settings.smtp_use_tls is False
    assert settings.expose_verification_links is False
    assert settings.media_root == tmp_path / "media"
    assert settings.max_content_length == 12345