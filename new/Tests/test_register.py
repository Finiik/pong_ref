import pytest
import pygame
from Views.Register.Registeration_Form import RegisterForm

class DummyFont:
    def render(self, text, antialias, color):
        return pygame.Surface((100, 30))

@pytest.fixture
def form():
    pygame.init()
    screen = pygame.Surface((520, 640))
    font = DummyFont()
    return RegisterForm(screen, font)

def test_initial_state(form):
    assert form.username == ""
    assert form.password == ""
    assert form.active_input == "username"

def test_switch_input_on_tab(form):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB)
    form.handle_event(event)
    assert form.active_input == "password"

def test_username_input_adds_chars(form):
    form.active_input = "username"
    event = pygame.event.Event(pygame.KEYDOWN, unicode="u", key=pygame.K_u)
    form.handle_event(event)
    assert form.username == "u"

def test_password_input_adds_chars(form):
    form.active_input = "password"
    event = pygame.event.Event(pygame.KEYDOWN, unicode="p", key=pygame.K_p)
    form.handle_event(event)
    assert form.password == "p"

def test_backspace_removes_char_username(form):
    form.username = "user"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    form.handle_event(event)
    assert form.username == "use"

def test_backspace_removes_char_password(form):
    form.active_input = "password"
    form.password = "pass"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    form.handle_event(event)
    assert form.password == "pas"

def test_escape_returns_menu(form):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    result = form.handle_event(event)
    assert result == "menu"

def test_mouse_click_sets_username(form):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(form.username_rect.x + 5, form.username_rect.y + 5))
    form.handle_event(event)
    assert form.active_input == "username"

def test_mouse_click_sets_password(form):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(form.password_rect.x + 5, form.password_rect.y + 5))
    form.handle_event(event)
    assert form.active_input == "password"
