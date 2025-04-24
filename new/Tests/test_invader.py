import pytest
from Views.Games import SpaceInvader

def test_invader_score_increment():
    game = SpaceInvader.Game()
    game.reset_game()
    game.enemies.clear()
    enemy = {"rect": game.player.copy(), "dir": (0, 0)}
    enemy["rect"].y -= 10
    game.enemies.append(enemy["rect"])
    bullet = game.player.copy()
    bullet.y -= 10
    game.bullets = [bullet]
    game.update_game()
    assert game.score >= 10 or not game.enemies