from unittest.mock import MagicMock

import pytest
from werkzeug.security import generate_password_hash

from npcgen.auth.models import User
from npcgen.auth.services import AuthService


@pytest.fixture
def mock_user():
    return User(
        id=1,
        username="admin",
        password=generate_password_hash("password1"),
        email="admin@example.com",
    )


def test_authenticate_valid_credentials(mock_user):
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = mock_user
    auth_service = AuthService(user_dao_mock)
    user = auth_service.authenticate("admin", "password1")
    assert user is not None
    assert user.id == mock_user.id


def test_authenticate_invalid_credentials(mock_user):
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = mock_user
    auth_service = AuthService(user_dao_mock)
    user = auth_service.authenticate("admin", "wrong")
    assert user is None


def test_register_user(mock_user):
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = None
    user_dao_mock.get_user_by_email.return_value = None
    user_dao_mock.create_user.return_value = mock_user.id
    auth_service = AuthService(user_dao_mock)
    user_id = auth_service.register_user(
        User(username="admin", password="password1", email="admin@example.com")
    )
    assert user_id is not None
    assert isinstance(user_id, int)


def test_register_user_username_exists():
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = mock_user
    user_dao_mock.get_user_by_email.return_value = None
    auth_service = AuthService(user_dao_mock)
    try:
        auth_service.register_user(
            User(
                username="admin",
                password="password1",
                email="admin@example.com",
            )
        )
    except Exception as e:
        assert e.args[0] == ("username", "Username already exists")
    else:
        assert False


def test_register_user_email_exists():
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = None
    user_dao_mock.get_user_by_email.return_value = mock_user
    auth_service = AuthService(user_dao_mock)
    try:
        auth_service.register_user(
            User(
                username="admin",
                password="password1",
                email="admin@example.com",
            )
        )
    except Exception as e:
        assert e.args[0] == ("email", "Email already exists")
    else:
        assert False


def test_register_invalid_password():
    user_dao_mock = MagicMock()
    user_dao_mock.get_user_by_username.return_value = None
    user_dao_mock.get_user_by_email.return_value = None
    auth_service = AuthService(user_dao_mock)
    try:
        auth_service.register_user(
            User(username="admin", password="pass", email="admin@example.org")
        )
    except Exception as e:
        assert e.args[0] == (
            "password",
            "Password must be at least 8 characters long",
        )
    else:
        assert False
