import pygame
import os
import random
import Models.User
from db import db_config

# Константи
WIDTH, HEIGHT = 520, 640
GAME_WIDTH, GAME_HEIGHT = 400, 400
GAME_X, GAME_Y = (WIDTH - GAME_WIDTH) // 2, 100
FPS = 60

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 30
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
BULLET_WIDTH, BULLET_HEIGHT = 5, 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BORDER_COLOR = (100, 100, 100)

class Game:
    def __init__(self, user: Models.User.User = None):
        self.user = user
        self.best_score = db_config.get_best_score(self.user[0], 4) if self.user else 0  # 4 — ID гри SpaceInvader

        self.menu_music = pygame.mixer.Sound("music_menu.mp3")
        self.game_music = pygame.mixer.Sound("game_music.mp3")

        font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")
        self.BigFONT = pygame.font.Font(font_path, 36)
        self.MidFONT = pygame.font.Font(font_path, 22)
        self.SmallFONT = pygame.font.Font(font_path, 15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invader")
        self.clock = pygame.time.Clock()

        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.paused = False
        self.game_over = False

        self.player = pygame.Rect(GAME_X + GAME_WIDTH // 2 - PLAYER_WIDTH // 2,
                                  GAME_Y + GAME_HEIGHT - PLAYER_HEIGHT - 10,
                                  PLAYER_WIDTH, PLAYER_HEIGHT)
        self.bullets = []
        self.enemies = [pygame.Rect(GAME_X + x * 45 + 10, GAME_Y + y * 40 + 10, ENEMY_WIDTH, ENEMY_HEIGHT)
                        for y in range(3) for x in range(8)]
        self.enemy_dir = 1
        self.enemy_speed = 1
        self.bullet_speed = -5

    def draw_text_centered(self, text, font, y, color=WHITE):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surf, rect)

    def draw_text_left(self, text, font, x, y, color=WHITE):
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw_game(self):
        self.screen.fill(BLACK)

        # Верхній UI
        self.draw_text_centered(f"SCORE: {self.score}", self.BigFONT, 45)
        self.draw_text_centered(f"BEST SCORE: {self.best_score}", self.SmallFONT, 75)

        # Рамка
        pygame.draw.rect(self.screen, BORDER_COLOR,
                         (GAME_X - 2, GAME_Y - 2, GAME_WIDTH + 4, GAME_HEIGHT + 4), 2)

        # Гравець, кулі, вороги
        pygame.draw.rect(self.screen, GREEN, self.player)
        for b in self.bullets:
            pygame.draw.rect(self.screen, WHITE, b)
        for e in self.enemies:
            pygame.draw.rect(self.screen, RED, e)

        # Нижній UI
        if self.game_over:
            self.draw_text_centered("Game Over", self.BigFONT, HEIGHT // 2 - 50)
            self.draw_text_centered(f"Your score: {self.score}", self.MidFONT, HEIGHT // 2)
            self.draw_text_centered("Press R to restart or ESC to exit", self.MidFONT, HEIGHT // 2 + 30)
        elif self.paused:
            self.draw_text_centered("Paused", self.BigFONT, HEIGHT // 2)
            self.draw_text_centered("Press P to resume or R to restart", self.MidFONT, HEIGHT // 2 + 30)
        else:
            controls1 = ["A - left", "D - right", "SPACE - shoot"]
            controls2 = ["P - pause", "R - restart", "ESC - exit"]
            y_start = GAME_Y + GAME_HEIGHT + 15
            x_left = WIDTH // 4
            x_right = 3 * WIDTH // 4
            for i, txt in enumerate(controls1):
                self.draw_text_left(txt, self.MidFONT, x_left - self.MidFONT.size(txt)[0] // 2, y_start + i * 25)
            for i, txt in enumerate(controls2):
                self.draw_text_left(txt, self.MidFONT, x_right - self.MidFONT.size(txt)[0] // 2, y_start + i * 25)

        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player.left > GAME_X:
            self.player.move_ip(-5, 0)
        if keys[pygame.K_d] and self.player.right < GAME_X + GAME_WIDTH:
            self.player.move_ip(5, 0)

    def update_game(self):
        if self.game_over or self.paused:
            return

        # Рух куль
        for b in self.bullets:
            b.move_ip(0, self.bullet_speed)
        self.bullets = [b for b in self.bullets if b.bottom > GAME_Y]

        # Рух ворогів
        for e in self.enemies:
            e.move_ip(self.enemy_dir * self.enemy_speed, 0)
        if any(e.right >= GAME_X + GAME_WIDTH or e.left <= GAME_X for e in self.enemies):
            self.enemy_dir *= -1
            for e in self.enemies:
                e.move_ip(0, 10)

        # Перевірка зіткнень
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if b.colliderect(e):
                    self.bullets.remove(b)
                    self.enemies.remove(e)
                    self.score += 10
                    self.best_score = max(self.best_score, self.score)
                    break

    def run(self):
        self.running = True
        self.reset_game()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_SPACE and not self.paused:
                        bullet = pygame.Rect(self.player.centerx, self.player.top, BULLET_WIDTH, BULLET_HEIGHT)
                        self.bullets.append(bullet)

            if not self.game_over and not self.paused:
                self.handle_input()
                self.update_game()

            self.draw_game()
            self.clock.tick(FPS)

        if self.user:
            db_config.save_score(self.user[0], 4, self.best_score)
        return "game_over"

def run():
    Game().run()

if __name__ == "__main__":
    Game().run()
