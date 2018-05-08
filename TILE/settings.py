import pygame as pg
# game options and settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Tilemap Game!"
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

'''
Define some colors
'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (186, 55, 5)
DARKGREY = (40, 40, 40)
BGCOLOR = BROWN

'''
Player settings
'''
PLAYER_SPEED = 300
PLAYER_ROTATION_SPEED = 250
PLAYER_IMAGE = "manBlue_gun.png"
PLAYER_HIT_BOX = pg.Rect(0, 0, 35, 35)

'''
Wall 
'''
WALL_IMG = "element_green_square.png"

'''
Mobs
'''
MOB_IMAGE = "zoimbie1_hold.png"
MOB_SPEED = 150
MOB_HIT_BOX = pg.Rect(0, 0, 35, 35)

