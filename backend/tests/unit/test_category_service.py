from __future__ import annotations
from participium.core.exceptions import NotFoundError, ValidationError
from participium.models.category import Category
from participium.services.category_service import CategoryService
import pytest
from unittest.mock import Mock

def make_category() ->CategoryService:
    session = Mock()
    category_repository=Mock()
    return CategoryService(session, category_repository)

def category(category_id: int =1, name: str="Roads", is_active: bool = True):
    return Category(id=category_id, name=name, is_active=is_active)

@pytest.mark.unit
def test_list_categories_return_allList():
    service = make_category()
    reports = [category(), category(2)]
    service.category_repository.list_all.return_value = reports

    result = service.list_categories(active_only=True)

    assert result == reports
    service.category_repository.list_all.assert_called_once_with(active_only=True)

@pytest.mark.unit
def test_get_category_return_category():
    service = make_category()
    expected_category = category()
    service.category_repository.get_by_id.return_value = expected_category

    result = service.get_category(1)

    assert result == expected_category
    service.category_repository.get_by_id.assert_called_once_with(1)

@pytest.mark.unit
def test_get_category_raises_NotFoundError():
    service = make_category()
    service.category_repository.get_by_id.return_value = None
    
    with pytest.raises(NotFoundError):
        service.get_category(404)

@pytest.mark.unit
def test_create_category():
    service = make_category()
    expected_category = category()
    service.category_repository.get_by_name.return_value = None
    service.category_repository.add.return_value = expected_category

    result = service.create_category("Roads")

    assert result == expected_category
    added_category = service.category_repository.add.call_args.args[0]
    assert isinstance(added_category, Category)
    assert added_category.name =="Roads"
    assert added_category.is_active is True
    service.category_repository.get_by_name.assert_called_once_with("Roads")
    service.session.commit.assert_called_once()

@pytest.mark.parametrize(
    "name", ["", " "]
)

@pytest.mark.unit
def test_create_category_not_cleaned_name(name: str):
    service = make_category()

    with pytest.raises(ValidationError, match="Category name is required"):
        service.create_category(name)

    service.category_repository.get_by_name.assert_not_called()
    service.category_repository.add.assert_not_called()
    service.session.commit.assert_not_called()

@pytest.mark.unit
def test_create_category_already_exist():
    service = make_category()
    expected_category = category()
    service.category_repository.get_by_name.return_value = expected_category

    with pytest.raises(ValidationError, match="Category name already exists."):
        service.create_category("Roads")
    service.session.commit.assert_not_called()
    service.category_repository.add.assert_not_called()

@pytest.mark.unit
def test_update_category_when_duplicate_None():
    service = make_category()
    service.category_repository.get_by_name.return_value = None
    existing_category = category(1, "Old name")
    service.category_repository.get_by_id.return_value = existing_category

    result = service.update_category(1, name="Roads")
    assert result == existing_category
    assert existing_category.name=="Roads"
    service.category_repository.get_by_name.assert_called_once_with("Roads")
    service.session.commit.assert_called_once()
    
@pytest.mark.unit
def test_update_category_when_different_category_id_with_duplicate_id():
    service = make_category()
    service.category_repository.get_by_name.return_value = category(2, "lighting")
    existing_category = category()
    service.category_repository.get_by_id.return_value = existing_category

    with pytest.raises(ValidationError):
        service.update_category(1, name="Lighting")
    assert existing_category.name =="Roads"
    service.session.commit.assert_not_called()

@pytest.mark.unit
def test_update_category_when_is_active_is_None():
    service = make_category()
    existing_category = category()
    service.category_repository.get_by_id.return_value = existing_category

    result = service.update_category(1, is_active=False)

    assert result == existing_category
    service.session.commit.assert_called_once()
    assert existing_category.name == "Roads"
    assert existing_category.is_active is False
    service.category_repository.get_by_name.assert_not_called()

