from __future__ import annotations

import pytest

from participium.services.user_service import UserService
from participium.models.user import User
from participium.core.exceptions import ValidationError
from werkzeug.datastructures import FileStorage

EXISTING_USER = User(
    id=101,
    username="maria.verdi",
    first_name="Maria",
    last_name="Verdi",
    email="maria.verdi@example.com",
    password_hash="HASHED_PASSWORD_101",
    is_active=True,
    is_email_verified=True,
    email_notifications_enabled=False,
    profile_picture_path="old_profile_pic_path.jpg"
)

EXISTING_USER_B = User(
    id=102,
    username="luca.gialli",
    first_name="Luca",
    last_name="Gialli",
    email="luca.gialli@example.com",
    password_hash="HASHED_PASSWORD_102",
    is_active=True,
    is_email_verified=True
)

@pytest.fixture
def seed_update_profile_data() -> None:
    pass

# TC-10.1
def test_update_profile(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_username = "new_username"
    new_first_name = "Mario"
    new_last_name = "Rossi"
    new_email_notification_preference = True
    new_profile_picture = FileStorage(filename="new_picture_path.jpg", content_type="jpg")

    updated_user = user_service.update_profile(user, new_username, new_first_name, new_last_name, new_email_notification_preference, new_profile_picture)

    assert updated_user.username == new_username
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name
    assert updated_user.email_notifications_enabled == new_email_notification_preference
    assert updated_user.profile_picture_path == new_profile_picture.filename

# TC-10.2
def test_update_profile_all_None(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_username = None
    new_first_name = None
    new_last_name = None
    new_email_notification_preference = None
    new_profile_picture = None

    updated_user = user_service.update_profile(user, new_username, new_first_name, new_last_name, new_email_notification_preference, new_profile_picture)

    assert updated_user.username == user.username
    assert updated_user.first_name == user.first_name
    assert updated_user.last_name == user.last_name
    assert updated_user.email_notifications_enabled == user.email_notifications_enabled
    assert updated_user.profile_picture_path == user.profile_picture_path

# TC-10.3
def test_update_profile_already_existing_username_error(seed_update_profile_data: None) -> None:
    user_service = UserService()
    userA = EXISTING_USER
    userB = EXISTING_USER_B
    new_username = userB.username

    with pytest.raises(ValidationError):
        updated_userA = user_service.update_profile(userA, new_username, None, None, None, None)

# TC-10.4
def test_update_profile_already_existing_username_error(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_username = user.username

    updated_user = user_service.update_profile(user, new_username, None, None, None, None)

    assert updated_user.username == new_username

# TC-10.5
def test_update_profile_email_notification_preference(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_email_notification_preference = False
    
    updated_user = user_service.update_profile(user, None, None, None, new_email_notification_preference, None)

    assert updated_user.email_notifications_enabled == new_email_notification_preference
    assert updated_user.username == user.username
    assert updated_user.first_name == user.first_name
    assert updated_user.last_name == user.last_name
    assert updated_user.profile_picture_path == user.profile_picture_path

# TC-10.6
def test_update_profile_empty_username(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_username = ""
    
    updated_user = user_service.update_profile(user, new_username, None, None, None, None)

    assert updated_user.email_notifications_enabled == user.email_notifications_enabled
    assert updated_user.username == new_username
    assert updated_user.first_name == user.first_name
    assert updated_user.last_name == user.last_name
    assert updated_user.profile_picture_path == user.profile_picture_path

# TC-10.7
def test_update_profile_empty_first_name(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_first_name = ""
    
    updated_user = user_service.update_profile(user, None, new_first_name, None, None, None)

    assert updated_user.email_notifications_enabled == user.email_notifications_enabled
    assert updated_user.username == user.username
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == user.last_name
    assert updated_user.profile_picture_path == user.profile_picture_path

# TC-10.8
def test_update_profile_empty_last_name(seed_update_profile_data: None) -> None:
    user_service = UserService()
    user = EXISTING_USER
    new_last_name = ""
    
    updated_user = user_service.update_profile(user, None, None, new_last_name, None, None)

    assert updated_user.email_notifications_enabled == user.email_notifications_enabled
    assert updated_user.username == user.username
    assert updated_user.first_name == user.first_name
    assert updated_user.last_name == new_last_name
    assert updated_user.profile_picture_path == user.profile_picture_path