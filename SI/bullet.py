from PYTHON_MODULES.PYGAME.SI.settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, y_speed, sprite):
        if sprite == "player":
            self.groups = game.bullets
        if sprite == "alien":
            self.groups = game.mob_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((5, 25))
        self.image.fill(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = y_speed

    def update(self):
        self.rect.y += self.y_speed
        alien_and_player_bullet_collisions = pygame.sprite.groupcollide(self.game.bullets, self.game.mob_bullets, True,
                                                                        True)
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or alien_and_player_bullet_collisions:
            self.kill()
