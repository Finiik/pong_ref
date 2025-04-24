import pytest
from Views.Games import Snake

def test_snake_reset_length():
    game = Snake.Game()
    game.reset_game()
    assert len(game.snake) == 3

def test_snake_movement():
    game = Snake.Game()
    game.reset_game()
    head_before = game.snake[0]
    game.direction = (1, 0)
    game.update_snake()
    head_after = game.snake[0]
    assert head_after != head_before

def test_snake_food_eat():
    game = Snake.Game()
    game.reset_game()
    game.snake[0] = game.food
    game.update_snake()
    assert game.score == 1 or len(game.snake) > 3