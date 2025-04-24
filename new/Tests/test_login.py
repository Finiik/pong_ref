import pytest
import pygame
from Views.Register.Login_Form import LoginForm

class DummyFont:
    def render(self, text, antialias, color):
        return pygame.Surface((100, 30))

@pytest.fixture
def form():
    pygame.init()
    screen = pygame.Surface((520, 640))
    font = DummyFont()
    return LoginForm(screen, font)

def test_initial_state(form):
    assert form.username == ""
    assert form.password == ""
    assert form.active_input == "username"

def test_switch_input_on_tab(form):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB)
    form.handle_event(event)
    assert form.active_input == "password"

def test_backspace_removes_character_username(form):
    form.username = "TestUser"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    form.handle_event(event)
    assert form.username == "TestUse"

def test_backspace_removes_character_password(form):
    form.active_input = "password"
    form.password = "Secret"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    form.handle_event(event)
    assert form.password == "Secre"

def test_escape_returns_menu(form):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    result = form.handle_event(event)
    assert result == "menu"

def test_username_input_adds_characters(form):
    form.active_input = "username"
    event = pygame.event.Event(pygame.KEYDOWN, unicode="a", key=pygame.K_a)
    form.handle_event(event)
    assert form.username == "a"

def test_password_input_adds_characters(form):
    form.active_input = "password"
    event = pygame.event.Event(pygame.KEYDOWN, unicode="b", key=pygame.K_b)
    form.handle_event(event)
    assert form.password == "b"

def test_mouse_click_sets_active_username(form):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(form.username_rect.x + 5, form.username_rect.y + 5))
    form.handle_event(event)
    assert form.active_input == "username"

def test_mouse_click_sets_active_password(form):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(form.password_rect.x + 5, form.password_rect.y + 5))
    form.handle_event(event)
    assert form.active_input == "password"

def test_enter_calls_login(form, monkeypatch):
    called = {"value": False}
    monkeypatch.setattr(form, "login", lambda: called.update(value=True))
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    form.handle_event(event)
    assert called["value"]
