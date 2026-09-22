from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from flask import session

import participium.app as app_module
from participium.app import create_app
from participium.core.exceptions import ValidationError


def settings(tmp_path, auto_init_db=False, bootstrap_reference_data=False, bootstrap_demo_data=False):
    return SimpleNamespace(
        instance_path=tmp_path / "instance",
        secret_key="test-secret",
        max_content_length=1024,
        frontend_origin="http://localhost:5173",
        auto_init_db=auto_init_db,
        bootstrap_reference_data=bootstrap_reference_data,
        bootstrap_demo_data=bootstrap_demo_data,
        media_root=tmp_path / "media",
    )


@pytest.mark.unit
def test_create_app_configures_flask_app_and_extensions(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())

    test_settings = settings(tmp_path)

    app = create_app(test_settings)

    assert app.config["SECRET_KEY"] == "test-secret"
    assert app.config["MAX_CONTENT_LENGTH"] == 1024
    assert app.config["SETTINGS"] == test_settings
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert "container" in app.extensions

    app_module.open_connection.assert_called_once()
    app_module.AppContainer.assert_called_once_with(test_settings)
    app_module.init_swagger.assert_called_once_with(app)
    app_module.register_blueprints.assert_called_once_with(app)


@pytest.mark.unit
def test_create_app_initializes_database_and_seed_data_when_enabled(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "create_all", Mock())
    monkeypatch.setattr(app_module, "seed_reference_data", Mock())
    monkeypatch.setattr(app_module, "seed_demo_data", Mock())
    monkeypatch.setattr(app_module, "get_session", Mock(return_value=Mock()))
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())

    test_settings = settings(
        tmp_path,
        auto_init_db=True,
        bootstrap_reference_data=True,
        bootstrap_demo_data=True,
    )

    create_app(test_settings)

    app_module.create_all.assert_called_once()
    app_module.seed_reference_data.assert_called_once_with(app_module.get_session.return_value)
    app_module.seed_demo_data.assert_called_once_with(
        app_module.get_session.return_value,
        test_settings.media_root,
    )


@pytest.mark.unit
def test_create_app_skips_database_creation_when_auto_init_disabled(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "create_all", Mock())
    monkeypatch.setattr(app_module, "seed_reference_data", Mock())
    monkeypatch.setattr(app_module, "seed_demo_data", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())

    create_app(settings(tmp_path, auto_init_db=False))

    app_module.create_all.assert_not_called()
    app_module.seed_reference_data.assert_not_called()
    app_module.seed_demo_data.assert_not_called()


@pytest.mark.unit
def test_domain_error_handler_returns_json_error(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())

    def register_test_route(app):
        @app.get("/boom")
        def boom():
            raise ValidationError("Invalid input")

    monkeypatch.setattr(app_module, "register_blueprints", register_test_route)

    app = create_app(settings(tmp_path))
    app.config.update(TESTING=True)

    response = app.test_client().get("/boom")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input"}


@pytest.mark.unit
def test_not_found_handler_returns_json_error(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())

    app = create_app(settings(tmp_path))
    app.config.update(TESTING=True)

    response = app.test_client().get("/missing-route")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Resource not found."}


@pytest.mark.unit
def test_request_hook_loads_active_current_user(monkeypatch, tmp_path):
    active_user = SimpleNamespace(id=7, is_active=True)
    repository = Mock()
    repository.get_by_id.return_value = active_user

    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())
    monkeypatch.setattr(app_module, "get_session", Mock(return_value=Mock()))
    monkeypatch.setattr(app_module, "UserRepository", Mock(return_value=repository))

    app = create_app(settings(tmp_path))
    app.config.update(TESTING=True)

    @app.get("/current-user-test")
    def current_user_test():
        from flask import g

        return {"current_user_id": g.current_user.id if g.current_user else None}

    client = app.test_client()
    with client.session_transaction() as flask_session:
        flask_session["user_id"] = 7

    response = client.get("/current-user-test")

    assert response.status_code == 200
    assert response.get_json() == {"current_user_id": 7}
    repository.get_by_id.assert_called_once_with(7)


@pytest.mark.unit
def test_request_hook_removes_inactive_user_from_session(monkeypatch, tmp_path):
    inactive_user = SimpleNamespace(id=7, is_active=False)
    repository = Mock()
    repository.get_by_id.return_value = inactive_user

    monkeypatch.setattr(app_module, "open_connection", Mock())
    monkeypatch.setattr(app_module, "init_swagger", Mock())
    monkeypatch.setattr(app_module, "register_blueprints", Mock())
    monkeypatch.setattr(app_module, "AppContainer", Mock())
    monkeypatch.setattr(app_module, "get_session", Mock(return_value=Mock()))
    monkeypatch.setattr(app_module, "UserRepository", Mock(return_value=repository))

    app = create_app(settings(tmp_path))
    app.config.update(TESTING=True)

    @app.get("/session-test")
    def session_test():
        return {"has_user_id": "user_id" in session}

    client = app.test_client()
    with client.session_transaction() as flask_session:
        flask_session["user_id"] = 7

    response = client.get("/session-test")

    assert response.status_code == 200
    assert response.get_json() == {"has_user_id": False}