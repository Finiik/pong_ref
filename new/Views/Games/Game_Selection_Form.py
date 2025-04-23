import sqlite3
import pygame
from Views.Games.Pong import Game  # Make sure this is a class with a .run() method
import Models.User
from Views.Register import Select_Auth_Form  # Import the file with main_menu() 
# === Конфігурація ===
WIDTH, HEIGHT = 520, 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameSelector:
    def __init__(self, screen, font, user: Models.User.User):
        pygame.init()
        self.screen = screen
        self.font = font
        self.user = user
        pygame.display.set_caption("Game Selector")
        self.selected_game_index = 0
        self.games = self.load_games_from_db()
        self.clock = pygame.time.Clock()

    def load_games_from_db(self):
        conn = sqlite3.connect('game_scores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM games")
        games = cursor.fetchall()
        conn.close()
        return [game[0] for game in games]

    def _draw_text(self, text, y, font, color=WHITE):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_text(f"Hello {self.user[1]}!",50, self.font)

        self._draw_text("Select Game:", 100, self.font)

        for i, game in enumerate(self.games):
            color = (255, 255, 0) if i == self.selected_game_index else WHITE
            self._draw_text(f"{i + 1}: {game}", 150 + i * 40, self.font, color)

        self._draw_text("Press ENTER to start", HEIGHT - 60, self.font)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_selected_game()
                elif event.key == pygame.K_DOWN:
                    self.selected_game_index = (self.selected_game_index + 1) % len(self.games)
                elif event.key == pygame.K_UP:
                    self.selected_game_index = (self.selected_game_index - 1) % len(self.games)
                elif event.key == pygame.K_ESCAPE:
                    return False  # Trigger end of run loop
        return True

    def start_selected_game(self):
        selected_game = self.games[self.selected_game_index]
        print(f"Starting {selected_game}...")

        # Hide selector window before launching game
        self.screen.fill(BLACK)
        pygame.display.flip()

        if selected_game == "Pong":
            from Views.Games.Pong import Game  # ✅ Local import to avoid circular
            pong_game = Game(self.user)
             # Make sure Pong has a class with a .run() method
            result = pong_game.run()
            if result == "game_over":
                self.run()
        if selected_game == "Snake":
            from Views.Games.Snake import Game  # ✅ Local import to avoid circular
            snake_game = Game(self.user)
             # Make sure Pong has a class with a .run() method
            result = snake_game.run()
            if result == "game_over":
                self.run()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        Select_Auth_Form.main_menu()


if __name__ == "__main__":
    selector = GameSelector()
    selector.run()
