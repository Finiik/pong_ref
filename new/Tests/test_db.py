import pytest
from unittest.mock import patch
import new.database.db_config as db_config

@patch("database.db_config.sqlite3.connect")
def test_get_best_score(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [50]

    score = db_config.get_best_score(1, 2)
    assert score == 50

@patch("database.db_config.sqlite3.connect")
def test_save_score(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value
    db_config.save_score(1, 2, 100)
    mock_cursor.execute.assert_called()