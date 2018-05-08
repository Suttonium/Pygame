from PYTHON_MODULES.PYGAME.FLAPPY_BIRD.settings import *


class Bird(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.ascending = 15
        self.descending = 7.5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.rect.centery -= self.ascending
        else:
            self.rect.centery += self.descending


class Topipe(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.top_pipes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.height = random.randint(0, 500)
        self.image = pg.transform.scale(self.game.pipe_image, (UNIVERSAL_WIDTH, self.height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.centerx -= 3
        if self.rect.left <= -10:
            self.rect.left = WIDTH
            self.height = random.randint(0, 500)
            self.image = pg.transform.scale(self.image, (UNIVERSAL_WIDTH, self.height))


class Bottompipe(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.bottom_pipes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ground = HEIGHT
        self.height = random.randint(0, 100)
        self.bottom_height = self.ground - (self.height + 150)
        self.image = pg.transform.rotate(self.game.pipe_image, 180)
        self.image = pg.transform.scale(self.image, (UNIVERSAL_WIDTH, self.bottom_height))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.centerx -= 3
        if self.rect.left <= -10:
            self.rect.left = WIDTH
            self.bottom_height = self.ground - (self.height + 150)
            self.image = pg.transform.scale(self.image, (UNIVERSAL_WIDTH, self.bottom_height))
