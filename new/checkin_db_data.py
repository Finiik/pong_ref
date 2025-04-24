import pygame
from database import db_config

data = db_config.get_user_by_username("Player1")
db_config.save_score(data[0], 1, 100)
data2 = db_config.get_best_score(data[0], 1)
data3 = db_config.get_game_by_id(2)
data4 = db_config.get_all_data()

#db_config.create_game("Pong")
print(data)
print(data2)
print(data3)
print(data4)
