import pygame
from db import db_config

data = db_config.get_user_by_username("Player1")
data2 = db_config.get_best_score(1, 1)
print(data)
print(data2)
