import random

from PYTHON_MODULES.PYGAME.SI.settings import *


class Mystery(pygame.sprite.Sprite):
    def __init__(self, game, x, y, x_speed):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.score_board = [150, 250, 350]
        self.score = random.choice(self.score_board)
        self.image = pygame.transform.scale(self.game.mystery_image, (55, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x_movement = x_speed
        # self.random_choice = random.randrange(0, 1)

    def update(self):
        self.rect.centerx += self.x_movement
        if self.rect.centerx > WIDTH or self.rect.centerx < 0 or not self.alive():
            self.game.mystery_counter -= 1
            self.kill()
