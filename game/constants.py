import pygame

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

NUM_ENEMIES = 10
inversion_limit = 40
MAX_INV_TIME = 5
MAX_REVEALS = 2
REVEAL_DURATION = 1
INITIAL_LIVES = 3

ENEMY_COLORS = [
    (200, 50, 50),
    (200, 100, 50),
    (200, 200, 50),
    (100, 200, 50),
    (50, 200, 200),
    (50, 100, 200),
    (150, 50, 200),
    (255, 255, 0),
    (50, 255, 255),
    (255, 0, 255)
]

