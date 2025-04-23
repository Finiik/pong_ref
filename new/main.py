import pygame

from Views.Register import Select_Auth_Form  # Import the file with main_menu()
from db import db_config

# Initialize pygame and database
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Your Game")
font = pygame.font.SysFont("Arial", 30)

db_config.init_db()

def run_auth_flow():
    
    while True:
       Select_Auth_Form.main_menu()  # This will show the auth menu
        # if choice == "login":
        #     result = login_form.draw()
        #     if isinstance(result, int):  # User logged in successfully
        #         return result
        # elif choice == "register":
        #     register_form.draw()
        # elif choice is None:
        #     pygame.quit()
        #     exit()

# Start the authentication flow
user_id = run_auth_flow()
print(f"User logged in with ID: {user_id}")

# Now run your game here
# game = Game(user_id)
# game.run()
