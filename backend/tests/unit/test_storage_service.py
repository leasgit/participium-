from __future__ import annotations
import pytest
from unittest.mock import Mock
from pathlib import Path
from werkzeug.datastructures import FileStorage
from participium.services.storage_service import StorageService, LocalFileStorageService

@pytest.mark.unit
def test_StorageService_return_simulated_file():
    service = StorageService()
    upload_file = Mock()

    result = service.save(upload_file)

    assert result == "simulated-file"

@pytest.mark.unit
def test_localFileStorageService(tmp_path):
    service = LocalFileStorageService(tmp_path)
    upload_file = Mock()
    upload_file.filename = "a good picture.jpg"

    result = service.save(upload_file)

    assert result.endswith("_a_good_picture.jpg")
    assert len(result.split('_', 1)[0]) == 32

    upload_file.save.assert_called_once()
    destination = upload_file.save.call_args.args[0]

    assert destination.parent == tmp_path
    assert destination.name == result

@pytest.mark.unit
def test_localFileStorageService_default_name(tmp_path):
    service = LocalFileStorageService(tmp_path)
   
    upload_file = Mock()
    upload_file.filename = None

    result = service.save(upload_file)

    assert result.endswith("_attachment.bin")
    assert len(result.split('_', 1)[0]) == 32

    upload_file.save.assert_called_once()
    destination = upload_file.save.call_args.args[0]

    assert destination.parent == tmp_path
    assert destination.name == result