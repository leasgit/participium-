import pytest
from participium.repositories.user_repository import UserRepository
from participium.models.user import User

def test_user_persistence_and_retrieval(db_session):
    """Tests that UserRepository correctly saves a user to the DB"""
    repo = UserRepository(session=db_session)
    new_user = User(username="bruno", email="bruno@polito.it", password_hash="hash")
    
    repo.save(new_user)
    db_session.commit()
    
    retrieved = repo.find_by_identifier("bruno@polito.it")
    assert retrieved.username == "bruno"
    assert retrieved.id is not None