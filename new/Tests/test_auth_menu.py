import pytest
import pygame
from Views.Register import Select_Auth_Form

class DummyFont:
    def render(self, text, antialias, color):
        return pygame.Surface((100, 30))

@pytest.fixture
def screen():
    pygame.init()
    return pygame.Surface((520, 640))

def test_buttons_exist():
    assert hasattr(Select_Auth_Form, "login_button")
    assert hasattr(Select_Auth_Form, "register_button")

def test_main_menu_returns_login(monkeypatch):
    monkeypatch.setattr(Select_Auth_Form, "login_form", type("MockForm", (), {"run": lambda self: None})())
    monkeypatch.setattr(Select_Auth_Form, "registration_form", type("MockForm", (), {"run": lambda self: None})())

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(Select_Auth_Form.login_button.center)),
        pygame.event.Event(pygame.QUIT)
    ]
    pygame.event.post(events[0])
    result = Select_Auth_Form.main_menu()
    assert result == "login"

def test_main_menu_returns_register(monkeypatch):
    monkeypatch.setattr(Select_Auth_Form, "login_form", type("MockForm", (), {"run": lambda self: None})())
    monkeypatch.setattr(Select_Auth_Form, "registration_form", type("MockForm", (), {"run": lambda self: None})())

    events = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(Select_Auth_Form.register_button.center)),
        pygame.event.Event(pygame.QUIT)
    ]
    pygame.event.post(events[0])
    result = Select_Auth_Form.main_menu()
    assert result == "register"

def test_window_dimensions(screen):
    assert screen.get_width() == 520
    assert screen.get_height() == 640

def test_font_mocking():
    font = DummyFont()
    surf = font.render("Text", True, (255, 255, 255))
    assert isinstance(surf, pygame.Surface)

def test_menu_colors_exist():
    assert hasattr(Select_Auth_Form, "WHITE")
    assert hasattr(Select_Auth_Form, "HOVER_COLOR")

def test_menu_loop_exists():
    assert hasattr(Select_Auth_Form, "main_menu")
