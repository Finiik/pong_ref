import pygame
import os
import random
import Models.User
from db import db_config

# === Конфігурація ===

WIDTH, HEIGHT = 520, 640
GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT = 400, 400  # Розмір ігрового поля
GAME_FIELD_X, GAME_FIELD_Y = (WIDTH - GAME_FIELD_WIDTH) // 2, 100  # Центрування ігрового поля нижче рахунку
GRID_SIZE = 10
GRID_WIDTH = GAME_FIELD_WIDTH // GRID_SIZE
GRID_HEIGHT = GAME_FIELD_HEIGHT // GRID_SIZE
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_START_LENGTH = 3
SNAKE_START_POSITION = (GRID_WIDTH // 4, GRID_HEIGHT // 2)
FOOD_START_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
GAME_SPEED = 10  # Кількість кадрів на секунду (швидкість змійки)

# Кольори RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = (100, 100, 100)

# === Ініціалізація Pygame ===
pygame.init()
pygame.mixer.init()

class Game:
    def __init__(self, user: Models.User.User = None):
        self.user = user

        self.best_score = db_config.get_best_score(self.user[0], 2) if self.user else 0 # 2 - ID гри "Змійка"
        self.menu_music = pygame.mixer.Sound("music_menu.mp3") # Замініть на власну музику
        self.game_music = pygame.mixer.Sound("game_music.mp3") # Замініть на власну музику

        font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")
        self.BigFONT = pygame.font.Font(font_path, 36)
        self.MiddleFONT = pygame.font.Font(font_path, 22)
        self.schmalFONT = pygame.font.Font(font_path, 15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Local Game")
        self.clock = pygame.time.Clock()

        self.reset_game()

    def reset_game(self):
        self.snake = [(SNAKE_START_POSITION[0], SNAKE_START_POSITION[1] + i) for i in range(SNAKE_START_LENGTH)]
        self.food = self.create_food()
        self.direction = (1, 0)  # Початковий напрямок: праворуч
        self.score = 0
        self.game_over = False
        self.paused = False

    def create_food(self):
        while True:
            position = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
            if position not in self.snake:
                return position

    def blit_text_centered(self, text, font, y, color=WHITE):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def blit_text_left(self, text, font, x, y, color=WHITE):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_grid(self, surface):
        for x in range(0, GAME_FIELD_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, GAME_FIELD_HEIGHT))
        for y in range(0, GAME_FIELD_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, (50, 50, 50), (0, y), (GAME_FIELD_WIDTH, y))

    def draw_game(self):
        self.screen.fill(BLACK)

        # UI над ігровим полем
        ui_y_top = 45
        self.blit_text_centered(f"Score: {self.score}", self.BigFONT, ui_y_top)
        self.blit_text_centered(f"Best score: {self.best_score}", self.schmalFONT, ui_y_top + 30)

        # Ігрова поверхня
        game_surface = pygame.Surface((GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT))
        game_surface.fill(BACKGROUND_COLOR)
        # self.draw_grid(game_surface) # Розкоментуйте, щоб побачити сітку на ігровому полі

        for segment in self.snake:
            pygame.draw.rect(game_surface, SNAKE_COLOR,
                             (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(game_surface, FOOD_COLOR,
                         (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Малюємо рамку навколо ігрового поля
        pygame.draw.rect(self.screen, BORDER_COLOR,
                         (GAME_FIELD_X - 2, GAME_FIELD_Y - 2, GAME_FIELD_WIDTH + 4, GAME_FIELD_HEIGHT + 4), 2)

        # Накладаємо ігрову поверхню на головний екран
        self.screen.blit(game_surface, (GAME_FIELD_X, GAME_FIELD_Y))

        # UI під ігровим полем
        ui_y_start = GAME_FIELD_Y + GAME_FIELD_HEIGHT + 15
        if self.game_over:
            self.blit_text_centered("Game Over", self.BigFONT, HEIGHT // 2 - 50)
            self.blit_text_centered(f"Your final score: {self.score}", self.MiddleFONT, HEIGHT // 2)
            self.blit_text_centered("Press R to restart or ESC to exit", self.MiddleFONT, HEIGHT // 2 + 30)
        elif self.paused:
            self.blit_text_centered("Paused", self.BigFONT, HEIGHT // 2)
            self.blit_text_centered("Press P to continue or R to restart", self.MiddleFONT, HEIGHT // 2 + 30)
        else:
            controls1 = ["W - up", "S - down", "A - left", "D - right"]
            controls2 = ["P - pause", "R - restart", "ESC - exit"]
            control_y = ui_y_start + 5
            control_x_left = WIDTH // 4
            control_x_right = 3 * WIDTH // 4
            line_height = 25

            for i, txt in enumerate(controls1):
                self.blit_text_left(txt, self.MiddleFONT, control_x_left - self.MiddleFONT.size(txt)[0] // 2, control_y + i * line_height)
            for i, txt in enumerate(controls2):
                self.blit_text_left(txt, self.MiddleFONT, control_x_right - self.MiddleFONT.size(txt)[0] // 2, control_y + i * line_height)

        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif keys[pygame.K_s] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif keys[pygame.K_a] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif keys[pygame.K_d] and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update_snake(self):
        if self.game_over or self.paused:
            return

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Перевірка на зіткнення зі стінами
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return

        # Перевірка на зіткнення з собою
        if new_head in self.snake[1:]:
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return

        self.snake.insert(0, new_head)

        # Перевірка, чи з'їла змійка їжу
        if self.snake[0] == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()

    def run(self):
        self.running = True
        self.reset_game()

        while self.running:
            self.handle_events()
            if not self.game_over and not self.paused:
                self.handle_input()
                self.update_snake()
            self.draw_game()
            self.clock.tick(GAME_SPEED)

        if self.user:
            db_config.save_score(self.user[0], 2, self.best_score)
        return "game_over"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_game()

if __name__ == "__main__":
    # Для тестування без авторизації користувача
    Game().run()