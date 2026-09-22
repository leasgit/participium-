from __future__ import annotations
from participium.models.category import Category
from participium.repositories.category_repository import CategoryRepository
import pytest
from unittest.mock import Mock

@pytest.fixture
def session():
    return Mock()

@pytest.fixture
def repository(session):
    return CategoryRepository(session)

def compiled_sql(statement) -> str:
    return str(statement.compile(compile_kwargs={"literal_binds": True}))

@pytest.mark.unit
def test_add_and_return_category(repository, session):
    category = Mock(spec=Category)

    result = repository.add(category)

    assert result is category
    session.add.assert_called_once_with(category)

@pytest.mark.unit
def test_get_by_id_uses_session_get(repository, session):
    category = Mock(spec=Category)
    session.get.return_value = category

    result = repository.get_by_id(category_id=7)

    assert result is category
    session.get.assert_called_once_with(Category, 7)


@pytest.mark.unit
def test_get_by_name_queries_category_name(repository, session):
    category = Mock(spec=Category)
    session.scalar.return_value = category

    result = repository.get_by_name("Roads")

    assert result is category
    sql = compiled_sql(session.scalar.call_args.args[0])
    assert "categories.name = 'Roads'" in sql


@pytest.mark.unit
def test_list_all_returns_categories_ordered_by_name(repository, session):
    categories = [Mock(spec=Category), Mock(spec=Category)]
    session.scalars.return_value = categories

    result = repository.list_all()

    assert result == categories
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "WHERE" not in sql
    assert "ORDER BY categories.name ASC" in sql


@pytest.mark.unit
def test_list_all_active_only_filters_active_categories(repository, session):
    categories = [Mock(spec=Category)]
    session.scalars.return_value = categories

    result = repository.list_all(active_only=True)

    assert result == categories
    sql = compiled_sql(session.scalars.call_args.args[0])
    assert "categories.is_active IS true" in sql
    assert "ORDER BY categories.name ASC" in sql
