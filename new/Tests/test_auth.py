import pytest
from unittest.mock import patch
from Views.Register import Registeration_Form

@patch("Views.Register.Registeration_Form.db_config")
def test_register_success(mock_db):
    mock_db.check_user_exists.return_value = False
    mock_db.add_user.return_value = True

    result = Registeration_Form.register_user("user", "pass")
    assert result == "Registration successful"

@patch("Views.Register.Registeration_Form.db_config")
def test_register_user_exists(mock_db):
    mock_db.check_user_exists.return_value = True

    result = Registeration_Form.register_user("user", "pass")
    assert result == "User already exists"

@patch("Views.Register.Registeration_Form.db_config")
def test_login_success(mock_db):
    mock_db.check_credentials.return_value = True

    result = Registeration_Form.login_user("user", "pass")
    assert result == "Login successful"

@patch("Views.Register.Registeration_Form.db_config")
def test_login_failure(mock_db):
    mock_db.check_credentials.return_value = False

    result = Registeration_Form.login_user("user", "pass")
    assert result == "Invalid credentials"