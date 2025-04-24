import pytest
import pygame
from Views.Games import Snake

@pytest.fixture
def game():
    pygame.init()
    return Snake.Game()

def test_initial_snake_length(game):
    assert len(game.snake) == Snake.SNAKE_START_LENGTH

def test_snake_initial_direction(game):
    assert game.direction == (1, 0)

def test_snake_does_not_collide_itself_initially(game):
    assert game.snake[0] not in game.snake[1:]

def test_snake_moves_correctly(game):
    head_before = game.snake[0]
    game.update_snake()
    head_after = game.snake[0]
    assert head_after != head_before

def test_food_not_on_snake(game):
    assert game.food not in game.snake

def test_collision_wall_triggers_game_over(game):
    game.snake[0] = (0, 0)
    game.direction = (-1, 0)  # Вліво — зіткнення зі стіною
    game.update_snake()
    assert game.game_over


def test_self_collision_triggers_game_over(game):
    game.snake = [(1, 1), (2, 1), (1, 1)]  # Самозіткнення
    game.update_snake()
    assert game.game_over

def test_snake_eats_food(game):
    game.food = (game.snake[0][0] + 1, game.snake[0][1])
    game.direction = (1, 0)
    game.update_snake()
    assert game.score == 1

def test_pause_toggle(game):
    game.paused = False
    game.paused = not game.paused
    assert game.paused

def test_restart_resets_score(game):
    game.score = 99
    game.reset_game()
    assert game.score == 0
