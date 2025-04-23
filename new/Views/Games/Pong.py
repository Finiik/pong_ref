import pygame  # Імпорт бібліотеки для розробки ігор
import os  # Для роботи з файловою системою
import random  # Для генерації випадкових напрямків м’яча
import Models.User
from db import db_config # Імпорт модуля для роботи з базою даних

# === Конфігурація ===

WIDTH, HEIGHT = 520, 640  # Повний розмір вікна
GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT = 250, 350  # Розмір ігрового поля
GAME_FIELD_X, GAME_FIELD_Y = 135, 80  # Відступ ігрового поля від країв екрана

BALL_SIZE = 9  # Розмір м’яча
PLATFORM_WIDTH = 50  # Ширина платформи
PLATFORM_HEIGHT = 10  # Висота платформи
BALL_SPEED = 3  # Швидкість м’яча
PLATFORM_SPEED = 5  # Швидкість платформи

# Кольори RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (0, 196, 156)
PLATFORM_COLOR = (118, 0, 196)

# === Ініціалізація Pygame ===
pygame.init()  # Ініціалізація всіх модулів Pygame
pygame.mixer.init()  # Ініціалізація аудіо

class Game:
    def __init__(self, user: Models.User.User):
        self.user = user
    
        self.best_score = db_config.get_best_score(self.user[0], 1)
        # Завантаження музики
        self.menu_music = pygame.mixer.Sound("music_menu.mp3")
        self.game_music = pygame.mixer.Sound("game_music.mp3")

        # Завантаження шрифтів
        font_path = os.path.join("./", "MinecraftTen-VGORe.ttf")
        self.BigFONT = pygame.font.Font(font_path, 36)
        self.MiddleFONT = pygame.font.Font(font_path, 22)
        self.schmalFONT = pygame.font.Font(font_path, 15)

        # Створення вікна
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Local Game")
        self.clock = pygame.time.Clock()  # Для контролю частоти кадрів

        self.reset_game()  # Початкове скидання гри

    def reset_game(self):
        # Початкова позиція м’яча та платформи
        self.ball = [GAME_FIELD_WIDTH // 2, GAME_FIELD_HEIGHT // 2]
        self.ball_dir = [random.choice([-1, 1]) * BALL_SPEED, -BALL_SPEED]
        self.player_pos = GAME_FIELD_WIDTH // 2 - PLATFORM_WIDTH // 2
        self.score = 0

    def blit_text_centered(self, text, font, y, color=WHITE):
        # Відображення тексту по центру
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def draw_game(self):
        self.screen.fill(BLACK)  # Очистити екран

        # Малюємо рамку навколо поля
        pygame.draw.rect(self.screen, WHITE,
                         (GAME_FIELD_X - 2, GAME_FIELD_Y - 2, GAME_FIELD_WIDTH + 4, GAME_FIELD_HEIGHT + 4))

        # Ігрова поверхня (всередині поля)
        game_surface = pygame.Surface((GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT))
        game_surface.fill(BLACK)

        # Малюємо м’яч та платформу
        pygame.draw.rect(game_surface, WHITE, (*self.ball, BALL_SIZE, BALL_SIZE))
        pygame.draw.rect(game_surface, WHITE,
                         (self.player_pos, GAME_FIELD_HEIGHT - 20, PLATFORM_WIDTH, PLATFORM_HEIGHT))

        # Накладаємо поверхню гри на екран
        self.screen.blit(game_surface, (GAME_FIELD_X, GAME_FIELD_Y))

        # UI
        self.blit_text_centered(f"Score: {self.score}", self.BigFONT, GAME_FIELD_Y + GAME_FIELD_HEIGHT - 400)
        self.blit_text_centered(f"Best score: {self.best_score}", self.schmalFONT, GAME_FIELD_Y + GAME_FIELD_HEIGHT - 370)

        # Інструкції
        controls = [
            "Space - start game",
            "A - left",
            "D - right",
            "P - pause",
            "R - restart",
            "ESC - exit"
        ]
        for i, txt in enumerate(controls):
            self.blit_text_centered(txt, self.MiddleFONT, GAME_FIELD_Y + GAME_FIELD_HEIGHT + 50 + i * 25)

        pygame.display.flip()  # Оновити дисплей

    def is_ball_out_of_bounds(self):
        # Перевірка, чи м’яч вийшов за межі поля
        return self.ball[1] >= GAME_FIELD_HEIGHT

    def handle_input(self):
        # Обробка натискань клавіш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_pos -= PLATFORM_SPEED
        if keys[pygame.K_d]:
            self.player_pos += PLATFORM_SPEED

        # Обмеження руху платформи в межах поля
        self.player_pos = max(0, min(GAME_FIELD_WIDTH - PLATFORM_WIDTH, self.player_pos))

    def update_ball(self):
        # Оновлення позиції м’яча
        self.ball[0] += self.ball_dir[0]
        self.ball[1] += self.ball_dir[1]

        # Відбиття від стін
        if self.ball[0] <= 0 or self.ball[0] >= GAME_FIELD_WIDTH - BALL_SIZE:
            self.ball_dir[0] *= -1
        if self.ball[1] <= 0:
            self.ball_dir[1] *= -1

        # Колізія з платформою
        ball_rect = pygame.Rect(self.ball[0], self.ball[1], BALL_SIZE, BALL_SIZE)
        platform_rect = pygame.Rect(self.player_pos, GAME_FIELD_HEIGHT - 20, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        if ball_rect.colliderect(platform_rect):
            self.ball_dir[1] *= -1
            self.score += 1
            self.best_score = max(self.best_score, self.score)

        # Програш — м’яч вийшов вниз
        if self.ball[1] >= GAME_FIELD_HEIGHT:
            self.reset_game()

    def run(self):
        self.running = True
        self.paused = False
        self.start_game()

    def start_game(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.handle_input()
                self.update_ball()
            self.draw_game()
            self.clock.tick(60)
        db_config.save_score(self.user[0], 1, self.best_score)  # Оновлення найкращого рахунку в базі даних
        return "game_over"        

    def handle_events(self):
        # Обробка ігрових подій
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
                elif event.key == pygame.K_SPACE and self.paused:
                    self.paused = False

if __name__ == "__main__":
    Game().run()
