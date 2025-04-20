import unittest
import pygame
import sys
import os

# Додамо шлях до основного модуля, якщо тест окремо
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from main import Game, GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT, BALL_SIZE, PLATFORM_WIDTH

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # Мінімальне вікно для Pygame
        self.game = Game()

    def tearDown(self):
        pygame.quit()

    def test_initial_score(self):
        self.assertEqual(self.game.score, 0)

    def test_initial_best_score(self):
        self.assertEqual(self.game.best_score, 0)

    def test_ball_position_on_reset(self):
        self.game.reset_game()
        self.assertEqual(self.game.ball, [GAME_FIELD_WIDTH // 2, GAME_FIELD_HEIGHT // 2])

    def test_player_position_on_reset(self):
        self.game.reset_game()
        expected = GAME_FIELD_WIDTH // 2 - PLATFORM_WIDTH // 2
        self.assertEqual(self.game.player_pos, expected)

    def test_ball_direction_is_valid(self):
        self.game.reset_game()
        x_dir, y_dir = self.game.ball_dir
        self.assertIn(x_dir, [-3, 3])
        self.assertEqual(y_dir, -3)

    def test_ball_bounces_off_left_wall(self):
        self.game.ball = [0, 100]
        self.game.ball_dir = [-3, -3]
        self.game.update_ball()
        self.assertEqual(self.game.ball_dir[0], 3)

    def test_ball_bounces_off_right_wall(self):
        self.game.ball = [GAME_FIELD_WIDTH - BALL_SIZE, 100]
        self.game.ball_dir = [3, -3]
        self.game.update_ball()
        self.assertEqual(self.game.ball_dir[0], -3)

    def test_ball_bounces_off_top(self):
        self.game.ball = [100, 0]
        self.game.ball_dir = [3, -3]
        self.game.update_ball()
        self.assertEqual(self.game.ball_dir[1], 3)

    def test_score_increases_on_hit(self):
        self.game.ball = [self.game.player_pos + 10, GAME_FIELD_HEIGHT - 21]
        self.game.ball_dir = [0, 3]
        old_score = self.game.score
        self.game.update_ball()
        self.assertEqual(self.game.score, old_score + 1)

    def test_best_score_updates(self):
        self.game.score = 5
        self.game.best_score = 3
        self.game.update_ball()
        self.assertEqual(self.game.best_score, 5)

    def test_ball_out_of_bounds_triggers_reset(self):
        self.game.ball[1] = GAME_FIELD_HEIGHT + 10
        self.game.update_ball()
        self.assertEqual(self.game.ball, [GAME_FIELD_WIDTH // 2, GAME_FIELD_HEIGHT // 2])

    def test_handle_input_left(self):
        self.game.player_pos = 100
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
        self.game.handle_input()
        self.assertLessEqual(self.game.player_pos, 100)

    def test_handle_input_right(self):
        self.game.player_pos = 100
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
        self.game.handle_input()
        self.assertGreaterEqual(self.game.player_pos, 100)

    def test_platform_does_not_go_left_outside(self):
        self.game.player_pos = 0
        self.game.handle_input()
        self.assertGreaterEqual(self.game.player_pos, 0)

    def test_platform_does_not_go_right_outside(self):
        self.game.player_pos = GAME_FIELD_WIDTH
        self.game.handle_input()
        self.assertLessEqual(self.game.player_pos, GAME_FIELD_WIDTH - PLATFORM_WIDTH)

    def test_pause_toggle(self):
        self.game.paused = False
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.game.handle_events()
        self.assertTrue(self.game.paused)

    def test_restart_resets_score(self):
        self.game.score = 10
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
        self.game.handle_events()
        self.assertEqual(self.game.score, 0)

    def test_escape_quits(self):
        self.game.running = True
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.game.handle_events()
        self.assertFalse(self.game.running)

    def test_space_unpauses(self):
        self.game.paused = True
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.game.handle_events()
        self.assertFalse(self.game.paused)

    def test_menu_selection_switches_state(self):
        self.game.in_menu = True
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.game.show_menu()
        self.assertFalse(self.game.in_menu)

    def test_draw_text_center_does_not_crash(self):
        try:
            self.game.draw_text_center("Hello", self.game.BigFONT, 100)
        except Exception as e:
            self.fail(f"draw_text_center raised an exception: {e}")

    def test_reset_game_sets_score_to_zero(self):
        self.game.score = 99
        self.game.reset_game()
        self.assertEqual(self.game.score, 0)

    def test_ball_collides_and_bounces(self):
        self.game.ball = [self.game.player_pos + 10, GAME_FIELD_HEIGHT - 21]
        self.game.ball_dir = [0, 3]
        self.game.update_ball()
        self.assertLess(self.game.ball_dir[1], 0)

    def test_draw_game_does_not_crash(self):
        try:
            self.game.draw_game()
        except Exception as e:
            self.fail(f"draw_game crashed: {e}")

    def test_show_menu_does_not_crash(self):
        try:
            self.game.show_menu()
        except Exception as e:
            self.fail(f"show_menu crashed: {e}")
