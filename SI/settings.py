import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
BACKGROUND = "background.jpg"
HS_FILE = "highscore.txt"

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# player
PLAYER_IMAGE = "player_ship.png"

# mobs
IMAGES = "Images"
TOP_MOB_IMAGE = "top.png"
TOP_IMAGE_2 = "top_alien_2.png"
MIDDLE_MOB_IMAGE = "second.png"
MIDDLE_MOB_IMAGE_2 = "middle_alien_image_2.png"
BOTTOM_MOB_IMAGE = "third.png"
BOTTOM_MOB_IMAGE_2 = "bottom_alien_2.png"
MYSTERY = "mystery.png"

# Sounds
SOUNDS = "Sounds"
EXPLOSION_1 = "Explosion4.wav"
EXPLOSION_2 = "Explosion8.wav"
LASER = "Laser_Shoot3.wav"
MYSTERY_SPAWN_SOUND = "mystery_spawn.wav"

# Fonts
font_name = pygame.font.match_font("arial")
