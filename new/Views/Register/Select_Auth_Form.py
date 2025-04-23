import pygame
import sys
from Views.Register.Registeration_Form import RegisterForm
from Views.Register.Login_Form import LoginForm
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Auth Menu")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 196, 156)
HOVER_COLOR = (0, 230, 180)

# Button setup
login_button = pygame.Rect(300, 250, 200, 60)
register_button = pygame.Rect(300, 350, 200, 60)
registration_form = RegisterForm(screen, font)  
login_form = LoginForm(screen, font)

def draw_button(rect, text, is_hovered):
    color = HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Welcome", True, WHITE)
        screen.blit(title, title.get_rect(center=(400, 120)))

        mouse_pos = pygame.mouse.get_pos()
        draw_button(login_button, "Login", login_button.collidepoint(mouse_pos))
        draw_button(register_button, "Register", register_button.collidepoint(mouse_pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    login_form.run()
                    print("Login selected")
                    return "login"
                elif register_button.collidepoint(event.pos):
                    registration_form.run()
                    print("Register selected")
                    return "register"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    choice = main_menu()
    print(f"User chose: {choice}")
