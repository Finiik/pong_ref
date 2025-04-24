# ... (всі імпорти як раніше)
import pygame
import os
import random
import Models.User
from db import db_config

CELL_SIZE = 20
ROWS = 21
COLS = 19
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
RED = (255, 0, 0)
BORDER_COLOR = (100, 100, 100)

WIDTH, HEIGHT = 520, 640
GAME_FIELD_X, GAME_FIELD_Y = (WIDTH - GRID_WIDTH) // 2, 100

level = [
    "1111111111111111111",
    "1000001000001000001",
    "1011101011101011101",
    "1000000000000000001",
    "1010111011101011101",
    "1000101000101000101",
    "1111101111101111101",
    "1000000000000000001",
    "1111101111111111101",
    "1000001000001000001",
    "1011101011101011101",
    "1000000000000000001",
    "1010111011101011101",
    "1000101000101000101",
    "1111101111101111101",
    "1000000000000000001",
    "1011101011101011101",
    "1000001000001000001",
    "1011111111111111101",
    "1000000000000000001",
    "1111111111111111111"
]

class Game:
    def __init__(self, user: Models.User.User = None):
        self.user = user
        self.best_score = db_config.get_best_score(self.user[0], 3) if self.user else 0
        font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")
        self.BigFONT = pygame.font.Font(font_path, 36)
        self.MiddleFONT = pygame.font.Font(font_path, 22)
        self.SmallFONT = pygame.font.Font(font_path, 15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.pacman = pygame.Rect(GAME_FIELD_X + 40, GAME_FIELD_Y, CELL_SIZE, CELL_SIZE)
        self.direction = pygame.Vector2(0, 0)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.dots = []
        self.enemies = []

        for row_index, row in enumerate(level):
            for col_index, cell in enumerate(row):
                if cell == "0":
                    self.dots.append(
                        pygame.Rect(
                            GAME_FIELD_X + col_index * CELL_SIZE,
                            GAME_FIELD_Y + row_index * CELL_SIZE,
                            6,
                            6
                        )
                    )
                    if random.random() < 0.01:
                        self.enemies.append({
                            "rect": pygame.Rect(
                                GAME_FIELD_X + col_index * CELL_SIZE,
                                GAME_FIELD_Y + row_index * CELL_SIZE,
                                CELL_SIZE, CELL_SIZE
                            ),
                            "dir": random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                        })

    def draw_text_centered(self, text, font, y, color=WHITE):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surf, rect)

    def draw_game(self):
        self.screen.fill(BLACK)
        self.draw_text_centered(f"SCORE: {self.score}", self.BigFONT, 45)
        self.draw_text_centered(f"BEST SCORE: {self.best_score}", self.SmallFONT, 75)
        pygame.draw.rect(self.screen, BORDER_COLOR,
                         (GAME_FIELD_X - 2, GAME_FIELD_Y - 2, GRID_WIDTH + 4, GRID_HEIGHT + 4), 2)

        for row_index, row in enumerate(level):
            for col_index, cell in enumerate(row):
                x = GAME_FIELD_X + col_index * CELL_SIZE
                y = GAME_FIELD_Y + row_index * CELL_SIZE
                if cell == "1":
                    pygame.draw.rect(self.screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

        for dot in self.dots:
            pygame.draw.circle(self.screen, PINK, dot.center, 3)

        pygame.draw.circle(self.screen, YELLOW, self.pacman.center, CELL_SIZE // 2)

        for enemy in self.enemies:
            pygame.draw.rect(self.screen, RED, enemy["rect"])

        if self.game_over:
            self.draw_text_centered("Game Over", self.BigFONT, HEIGHT // 2 - 50)
            self.draw_text_centered(f"Your score: {self.score}", self.MiddleFONT, HEIGHT // 2)
            self.draw_text_centered("Press R to restart or ESC to exit", self.MiddleFONT, HEIGHT // 2 + 30)
        elif self.paused:
            self.draw_text_centered("Paused", self.BigFONT, HEIGHT // 2)
            self.draw_text_centered("Press P to resume or R to restart", self.MiddleFONT, HEIGHT // 2 + 30)
        else:
            controls1 = ["W - up", "S - down", "A - left", "D - right"]
            controls2 = ["P - pause", "R - restart", "ESC - exit"]
            y_start = GAME_FIELD_Y + GRID_HEIGHT + 15
            for i, txt in enumerate(controls1 + controls2):
                x = WIDTH // 2 - 100 if i < 4 else WIDTH // 2 + 20
                y = y_start + (i % 4) * 25
                self.screen.blit(self.MiddleFONT.render(txt, True, WHITE), (x, y))

        pygame.display.flip()

    def update_pacman(self):
        if self.game_over or self.paused:
            return

        new_pos = self.pacman.move(self.direction)
        if self.can_move(new_pos):
            self.pacman = new_pos

        for dot in self.dots[:]:
            if self.pacman.colliderect(dot):
                self.dots.remove(dot)
                self.score += 10
                self.best_score = max(self.best_score, self.score)

        for enemy in self.enemies:
            if self.pacman.colliderect(enemy["rect"]):
                self.game_over = True

    def can_move(self, rect):
        col = (rect.x - GAME_FIELD_X) // CELL_SIZE
        row = (rect.y - GAME_FIELD_Y) // CELL_SIZE
        return 0 <= row < len(level) and 0 <= col < len(level[0]) and level[row][col] != "1"

    def update_enemies(self):
        for enemy in self.enemies:
            dx, dy = enemy["dir"]
            new_rect = enemy["rect"].move(dx * CELL_SIZE, dy * CELL_SIZE)
            if self.can_move(new_rect):
                enemy["rect"] = new_rect
            else:
                enemy["dir"] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def run(self):
        self.running = True
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
                    elif event.key == pygame.K_w:
                        self.direction = pygame.Vector2(0, -CELL_SIZE)
                    elif event.key == pygame.K_s:
                        self.direction = pygame.Vector2(0, CELL_SIZE)
                    elif event.key == pygame.K_a:
                        self.direction = pygame.Vector2(-CELL_SIZE, 0)
                    elif event.key == pygame.K_d:
                        self.direction = pygame.Vector2(CELL_SIZE, 0)

            if not self.paused and not self.game_over:
                self.update_pacman()
                self.update_enemies()

            self.draw_game()
            self.clock.tick(10)

        if self.user:
            db_config.save_score(self.user[0], 3, self.best_score)
        return "game_over"

def run():
    Game().run()

if __name__ == "__main__":
    Game().run()
