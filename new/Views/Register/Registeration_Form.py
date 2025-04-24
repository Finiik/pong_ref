import pygame
from db import db_config
import Models.User
import os  # Для роботи з файловою системою


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
ACTIVE_COLOR = (0, 200, 150)

class RegisterForm:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.username = ""
        self.password = ""
        self.active_input = "username"
        self.message = ""

        # Input field rects
        self.username_rect = pygame.Rect(65, 140, 300, 40)
        self.password_rect = pygame.Rect(65, 260, 300, 40)

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_text("Register", 50, 60)

        # Draw input labels
        self._draw_text("Username:", 90)
        self._draw_text("Password:", 210)

        # Draw input boxes
        self._draw_input_box(self.username_rect, self.username, self.active_input == "username")
        self._draw_input_box(self.password_rect, "*" * len(self.password), self.active_input == "password")

        # Instructions and messages
        self._draw_text("Press ENTER to register", 310)
        self._draw_text("Press ESC to go back", 350)
        self._draw_text(self.message, 350, color=(255, 50, 50))

        pygame.display.flip()

    def _draw_input_box(self, rect, text, active):
        color = ACTIVE_COLOR if active else GRAY
        pygame.draw.rect(self.screen, color, rect, 2)
        txt_surface = self.font.render(text, True, WHITE)
        self.screen.blit(txt_surface, (rect.x + 5, rect.y + 5))

    def _draw_text(self, text, y, color=WHITE):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (50, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_input = "password" if self.active_input == "username" else "username"
            elif event.key == pygame.K_RETURN:
                return self.register()
            elif event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            else:
                if self.active_input == "username":
                    self.username += event.unicode
                else:
                    self.password += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_input = "username"
            elif self.password_rect.collidepoint(event.pos):
                self.active_input = "password"

    def register(self):
        if db_config.get_user_by_username(self.username):
            self.message = "Username already exists!"
        else:
            db_config.create_user(self.username, self.password)
            user = db_config.get_user_by_username(self.username)
            self.message = "Registration successful!"
            from Views.Games.Game_Selection_Form import GameSelector
            GameSelector(self.screen, self.font, user).run()  # Start game selection after registration
            return "game_selection"
        return None

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result == "menu":
                    return "menu"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(60)
