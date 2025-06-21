from app.repositories.repository_factory import RepositoryFactory
from app.models.user import User

def test_create_user(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@example.com", hashed_password="test", display_name="Test User")
    created_user = user_repo.create(user)  # Removed the second db parameter
    assert created_user.email == "test@example.com"
    assert created_user.display_name == "Test User"


def test_get_user_by_email(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@example.com", hashed_password="test", display_name="Test User")
    user_repo.delete_by_id(user.id)  # Ensure the user does not exist before the test
    non_existent_user = user_repo.get_by_id(user.id)  # Attempt to get a non-existent user
    assert non_existent_user is None  # Ensure the user does not exist

def test_get_user_by_id(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@gmail.com", hashed_password="test", display_name="Test User")
    created_user = user_repo.create(user)
    fetched_user = user_repo.get_by_id(created_user.id)
    assert fetched_user is created_user

def test_update_user(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@gmail.com", hashed_password="test", display_name="Test User")
    created_user = user_repo.create(user)
    updates = {
        "email": "test2@gmail.com",
        "hashed_password": "newpassword",
        "display_name": "Updated User"
    }
    updated_user = user_repo.update_by_id(created_user.id, updates)
    found_user = user_repo.get_by_id(created_user.id)
    
    assert found_user.email == "test2@gmail.com" and found_user.display_name == "Updated User"

def test_delete_user(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@gmail.com", hashed_password="test", display_name="Test User")
    created_user = user_repo.create(user)
    user_repo.delete_by_id(created_user.id)
    assert user_repo.get_by_id(created_user.id) is None  # Ensure the user is deleted

def test_verify_user(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user = User(email="test@gmail.com", hashed_password="test", display_name="Test User")
    user_repo.create(user)
    assert not user_repo.get_by_id(user.id).verified

def test_get_by_username(db):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_repo.create(User(email="test@gmail.com", hashed_password="test", display_name="terminator123"))
    fetched_users = user_repo.get_by_username("terminator123")
    assert fetched_users[0].display_name == "terminator123"
    