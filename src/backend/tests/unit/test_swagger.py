from __future__ import annotations

from unittest.mock import Mock

import pytest

import participium.api.swagger as swagger


@pytest.mark.unit
def test_array_of_builds_array_schema_with_definition_reference():
    result = swagger._array_of("Photo")

    assert result == {
        "type": "array",
        "items": {"$ref": "#/definitions/Photo"},
    }


@pytest.mark.unit
def test_message_response_builds_message_schema():
    result = swagger._message_response("Operation completed.")

    assert result["type"] == "object"
    assert result["required"] == ["message"]
    assert result["properties"]["message"]["type"] == "string"
    assert result["properties"]["message"]["example"] == "Operation completed."


@pytest.mark.unit
def test_definitions_contains_core_api_models():
    definitions = swagger._definitions()

    assert "Error" in definitions
    assert "Health" in definitions
    assert "ReferenceData" in definitions
    assert "User" in definitions
    assert "ReportSummary" in definitions
    assert "ReportDetail" in definitions
    assert "Message" in definitions
    assert "Notification" in definitions
    assert "Statistics" in definitions


@pytest.mark.unit
def test_definitions_user_schema_contains_expected_fields_and_roles():
    user_schema = swagger._definitions()["User"]

    assert user_schema["type"] == "object"
    assert "id" in user_schema["required"]
    assert "username" in user_schema["required"]
    assert "email" in user_schema["required"]
    assert "role" in user_schema["required"]
    assert user_schema["properties"]["email"]["format"] == "email"
    assert user_schema["properties"]["role"]["enum"] == ["citizen", "operator", "admin"]


@pytest.mark.unit
def test_definitions_report_status_enum_is_reused_by_report_and_update_request():
    definitions = swagger._definitions()

    expected_statuses = [
        "pending_approval",
        "rejected",
        "assigned",
        "in_progress",
        "resolved",
    ]

    assert definitions["ReportSummary"]["properties"]["status"]["enum"] == expected_statuses
    assert definitions["UpdateStatusRequest"]["properties"]["status"]["enum"] == expected_statuses


@pytest.mark.unit
def test_init_swagger_passes_expected_template_to_flasgger(monkeypatch):
    swagger_constructor = Mock()
    fake_app = Mock()

    monkeypatch.setattr(swagger, "Swagger", swagger_constructor)

    swagger.init_swagger(fake_app)

    swagger_constructor.assert_called_once()
    assert swagger_constructor.call_args.args[0] == fake_app

    template = swagger_constructor.call_args.kwargs["template"]
    assert template["swagger"] == "2.0"
    assert template["info"]["title"] == "Participium API"
    assert template["basePath"] == "/api/v1"
    assert template["definitions"] == swagger._definitions()