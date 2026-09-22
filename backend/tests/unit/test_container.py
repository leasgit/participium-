from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import participium.container as container
from participium.container import AppContainer, ControllerBundle, get_controllers


@pytest.mark.unit
def test_app_container_initializes_shared_gateway_and_storage(monkeypatch, tmp_path):
    email_gateway = Mock()
    storage_service_class = Mock()

    monkeypatch.setattr(container, "build_email_gateway", Mock(return_value=email_gateway))
    monkeypatch.setattr(container, "LocalFileStorageService", storage_service_class)

    settings = SimpleNamespace(media_root=tmp_path)

    app_container = AppContainer(settings)

    assert app_container.settings == settings
    assert app_container.email_gateway == email_gateway
    container.build_email_gateway.assert_called_once_with(settings)
    storage_service_class.assert_called_once_with(tmp_path)


@pytest.mark.unit
def test_build_controllers_returns_controller_bundle_with_expected_repositories(monkeypatch, tmp_path):
    session = Mock()
    monkeypatch.setattr(container, "get_session", Mock(return_value=session))
    monkeypatch.setattr(container, "build_email_gateway", Mock(return_value=Mock()))
    monkeypatch.setattr(container, "LocalFileStorageService", Mock(return_value=Mock()))

    settings = SimpleNamespace(media_root=tmp_path)
    app_container = AppContainer(settings)

    bundle = app_container.build_controllers()

    assert isinstance(bundle, ControllerBundle)
    assert bundle.auth is not None
    assert bundle.users is not None
    assert bundle.reports is not None
    assert bundle.operators is not None
    assert bundle.admin is not None
    assert bundle.statistics is not None

    assert set(bundle.repositories.keys()) == {
        "users",
        "categories",
        "reports",
        "messages",
        "notifications",
        "tokens",
    }


@pytest.mark.unit
def test_build_controllers_uses_same_session_for_all_repositories(monkeypatch, tmp_path):
    session = Mock()
    monkeypatch.setattr(container, "get_session", Mock(return_value=session))
    monkeypatch.setattr(container, "build_email_gateway", Mock(return_value=Mock()))
    monkeypatch.setattr(container, "LocalFileStorageService", Mock(return_value=Mock()))

    settings = SimpleNamespace(media_root=tmp_path)
    app_container = AppContainer(settings)

    bundle = app_container.build_controllers()

    for repository in bundle.repositories.values():
        assert repository.session == session

    
from flask import Flask


@pytest.mark.unit
def test_get_controllers_delegates_to_container_registered_in_flask_app():
    flask_app = Flask(__name__)

    fake_bundle = Mock()
    fake_container = Mock()
    fake_container.build_controllers.return_value = fake_bundle

    flask_app.extensions["container"] = fake_container

    with flask_app.app_context():
        result = get_controllers()

    assert result == fake_bundle
    fake_container.build_controllers.assert_called_once()