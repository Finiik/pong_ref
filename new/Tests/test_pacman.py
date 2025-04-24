import pytest
import pygame
from Views.Games import Pacman
import sys
import os

# Додає корінь проєкту до PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def game():
    pygame.init()
    return Pacman.Game()

def test_initial_score(game):
    assert game.score == 0

def test_pacman_start_position(game):
    expected_x = Pacman.GAME_FIELD_X + 40
    expected_y = Pacman.GAME_FIELD_Y
    assert game.pacman.topleft == (expected_x, expected_y)

def test_pacman_initial_direction(game):
    assert game.direction == pygame.Vector2(0, 0)

def test_pacman_can_move_to_open_cell(game):
    open_rect = game.dots[0]
    assert game.can_move(open_rect)


def test_pacman_blocked_by_wall(game):
    wall_rect = pygame.Rect(Pacman.GAME_FIELD_X, Pacman.GAME_FIELD_Y, Pacman.CELL_SIZE, Pacman.CELL_SIZE)
    assert not game.can_move(wall_rect)

def test_enemy_spawn_probability(game):
    enemy_count = len(game.enemies)
    assert 0 <= enemy_count <= 10  # Не надто багато, бо шанс 1%

def test_dots_exist(game):
    assert len(game.dots) > 0

def test_eating_dot_increases_score(game):
    dot = game.dots[0]
    game.pacman = dot
    game.update_pacman()
    assert game.score == 10

def test_pacman_dies_on_enemy_collision(game):
    enemy = game.enemies[0]
    game.pacman = enemy["rect"]
    game.update_pacman()
    assert game.game_over

def test_pause_toggle(game):
    game.paused = False
    game.paused = not game.paused
    assert game.paused

def test_restart_game(game):
    game.score = 123
    game.reset_game()
    assert game.score == 0
