import pytest
from Views.Games import Pacman

def test_pacman_score_increment():
    game = Pacman.Game()
    game.reset_game()
    dot = game.dots[0]
    game.pacman.topleft = dot.topleft
    game.update_pacman()
    assert game.score >= 10

def test_pacman_hit_enemy_game_over():
    game = Pacman.Game()
    game.reset_game()
    if not game.enemies:
        return
    enemy = game.enemies[0]
    game.pacman.topleft = enemy["rect"].topleft
    game.update_pacman()
    assert game.game_over