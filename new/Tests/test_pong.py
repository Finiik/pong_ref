import pytest
import pygame
from Views.Games import Pong

@pytest.fixture
def game():
    pygame.init()
    return Pong.Game(user=("test", "Tester", "pass"))

def test_initial_score(game):
    assert game.score == 0

def test_ball_initial_position(game):
    x, y = game.ball
    assert 0 <= x <= Pong.GAME_FIELD_WIDTH
    assert 0 <= y <= Pong.GAME_FIELD_HEIGHT

def test_platform_initial_position(game):
    assert 0 <= game.player_pos <= Pong.GAME_FIELD_WIDTH - Pong.PLATFORM_WIDTH

def test_ball_bounce_horizontal(game):
    game.ball = [0, 100]  # Ліва межа
    game.ball_dir = [-3, -3]
    game.update_ball()
    assert game.ball_dir[0] > 0  # Має відбитися вправо

def test_ball_bounce_top(game):
    game.ball = [100, 0]  # Верхня межа
    game.ball_dir = [3, -3]
    game.update_ball()
    assert game.ball_dir[1] > 0  # Має відбитися вниз

def test_score_increases_on_hit(game):
    game.ball = [game.player_pos + 10, Pong.GAME_FIELD_HEIGHT - 25]
    game.ball_dir = [0, 3]
    game.update_ball()
    assert game.score == 1

def test_score_best_updated(game):
    # Робимо best_score гарантовано нижчим
    game.best_score = 0
    game.score = 0

    # М’яч на платформі — щоб точно була колізія
    game.ball = [game.player_pos + 10, Pong.GAME_FIELD_HEIGHT - 25]
    game.ball_dir = [0, 3]  # Напрямок вниз
    game.update_ball()

    assert game.best_score == 1


def test_ball_reset_on_loss(game):
    game.ball = [100, Pong.GAME_FIELD_HEIGHT + 1]  # Нижче межі
    game.update_ball()
    assert game.score == 0  # Гру скинуто

def test_pause_toggle(game):
    game.paused = False
    game.paused = not game.paused
    assert game.paused

def test_restart_resets_score(game):
    game.score = 99
    game.reset_game()
    assert game.score == 0
