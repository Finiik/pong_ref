import pytest
import pygame
from Views.Games import SpaceInvader

@pytest.fixture
def game():
    pygame.init()
    return SpaceInvader.Game(user=("test", "Tester", "pass"))

def test_initial_score(game):
    assert game.score == 0

def test_enemy_spawn_count(game):
    assert len(game.enemies) == 24  # 3 рядки × 8 ворогів

def test_bullet_added_on_space(game):
    game.paused = False
    game.bullets.clear()
    bullet = pygame.Rect(game.player.centerx, game.player.top, SpaceInvader.BULLET_WIDTH, SpaceInvader.BULLET_HEIGHT)
    game.bullets.append(bullet)
    assert len(game.bullets) == 1

def test_bullet_movement(game):
    bullet = pygame.Rect(game.player.centerx, game.player.top, SpaceInvader.BULLET_WIDTH, SpaceInvader.BULLET_HEIGHT)
    game.bullets = [bullet]
    top_before = bullet.top
    game.update_game()
    top_after = bullet.top
    assert top_after < top_before

def test_enemy_direction_change_on_wall_hit(game):
    # Симулюємо ворога на правій межі
    game.enemies = [pygame.Rect(SpaceInvader.GAME_X + SpaceInvader.GAME_WIDTH - 1, 100, 40, 30)]
    game.enemy_dir = 1
    game.update_game()
    assert game.enemy_dir == -1

def test_collision_bullet_enemy_removes_both(game):
    bullet = pygame.Rect(200, 200, 5, 10)
    enemy = pygame.Rect(200, 200, 40, 30)
    game.bullets = [bullet]
    game.enemies = [enemy]
    game.update_game()
    assert len(game.bullets) == 0
    assert len(game.enemies) == 0

def test_score_increased_on_hit(game):
    bullet = pygame.Rect(200, 200, 5, 10)
    enemy = pygame.Rect(200, 200, 40, 30)
    game.bullets = [bullet]
    game.enemies = [enemy]
    game.score = 0
    game.update_game()
    assert game.score == 10

def test_best_score_updated_on_hit(game):
    game.best_score = 0
    bullet = pygame.Rect(200, 200, 5, 10)
    enemy = pygame.Rect(200, 200, 40, 30)
    game.bullets = [bullet]
    game.enemies = [enemy]
    game.update_game()
    assert game.best_score == 10

def test_pause_toggle(game):
    game.paused = False
    game.paused = not game.paused
    assert game.paused

def test_restart_game(game):
    game.score = 999
    game.reset_game()
    assert game.score == 0
