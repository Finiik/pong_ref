import pytest
from Views.Games import Pong

def test_pong_initial_score():
    game = Pong.Game()
    assert game.left_score == 0
    assert game.right_score == 0

def test_pong_reset_ball():
    game = Pong.Game()
    game.reset_ball()
    assert -5 <= game.ball_speed[0] <= 5
    assert -5 <= game.ball_speed[1] <= 5