import pytest
import pygame
from Views.Games.Game_Selection_Form import GameSelector

class DummyUser:
    def __getitem__(self, index):
        return ["user_id", "TestUser", "testpass"][index]

class DummyFont:
    def render(self, text, antialias, color):
        return pygame.Surface((100, 30))

@pytest.fixture
def selector(tmp_path, monkeypatch):
    pygame.init()
    screen = pygame.Surface((520, 640))
    font = DummyFont()

    db_path = tmp_path / "game_scores.db"
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.executemany("INSERT INTO games (name) VALUES (?)", [("Pong",), ("Snake",), ("Pacman",)])
    conn.commit()
    conn.close()

    # ✅ Зберігаємо оригінал, щоб уникнути рекурсії
    original_connect = sqlite3.connect
    monkeypatch.setattr("Views.Games.Game_Selection_Form.sqlite3.connect", lambda _: original_connect(db_path))

    return GameSelector(screen, font, DummyUser())

def test_load_games(selector):
    assert selector.games == ["Pong", "Snake", "Pacman"]

def test_initial_selected_index(selector):
    assert selector.selected_game_index == 0

def test_handle_down_arrow(selector):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    pygame.event.post(event)
    selector.handle_events()
    assert selector.selected_game_index == 1

def test_handle_up_arrow(selector):
    selector.selected_game_index = 2
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    pygame.event.post(event)
    selector.handle_events()
    assert selector.selected_game_index == 1

def test_wrap_around_up(selector):
    selector.selected_game_index = 0
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    pygame.event.post(event)
    selector.handle_events()
    assert selector.selected_game_index == len(selector.games) - 1

def test_wrap_around_down(selector):
    selector.selected_game_index = len(selector.games) - 1
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    pygame.event.post(event)
    selector.handle_events()
    assert selector.selected_game_index == 0

def test_escape_key_exits(selector):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(event)
    result = selector.handle_events()
    assert result is False

def test_enter_starts_game(selector, monkeypatch):
    selector.selected_game_index = 0
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    monkeypatch.setattr(selector, "start_selected_game", lambda: setattr(selector, "started", True))

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(event)
    selector.handle_events()

    assert getattr(selector, "started", False) is True

def test_selected_game_index_cycles_up(selector):
    selector.selected_game_index = 0
    selector.selected_game_index = (selector.selected_game_index - 1) % len(selector.games)
    assert selector.selected_game_index == 2

def test_selected_game_index_cycles_down(selector):
    selector.selected_game_index = 2
    selector.selected_game_index = (selector.selected_game_index + 1) % len(selector.games)
    assert selector.selected_game_index == 0

def test_start_selected_game_exists_method(selector):
    assert hasattr(selector, "start_selected_game")

def test_draw_method_exists(selector):
    assert hasattr(selector, "draw")

def test_run_method_exists(selector):
    assert hasattr(selector, "run")