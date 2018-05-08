from PYTHON_MODULES.PYGAME.TILE.tilemap import *
vec = pg.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.velocity.x > 0:
                sprite.position.x = hits[0].rect.left - sprite.hit_box.width / 2
            if sprite.velocity.x < 0:
                sprite.position.x = hits[0].rect.right + sprite.hit_box.width / 2
            sprite.velocity.x = 0
            sprite.hit_box.centerx = sprite.position.x
    if direction == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.velocity.y > 0:
                sprite.position.y = hits[0].rect.top - sprite.hit_box.height / 2
            if sprite.velocity.y < 0:
                sprite.position.y = hits[0].rect.bottom + sprite.hit_box.height / 2
            sprite.velocity.y = 0
            sprite.hit_box.centery = sprite.position.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.center = self.rect.center
        self.velocity = vec(0, 0)
        self.position = vec(x, y) * TILESIZE
        self.rotation = 0  # 0 degrees because pointing along positive x-axis

    def get_keys(self):
        self.rotation_speed = 0
        self.velocity = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotation_speed = PLAYER_ROTATION_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotation_speed = -PLAYER_ROTATION_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.velocity = vec(PLAYER_SPEED, 0).rotate(-self.rotation)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.velocity = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rotation)
        # if self.velocity.x != 0 and self.velocity.y != 0:
        #     self.velocity *= 0.7071  # solves diagonal speed issue using sqrt of 2/pythagorean theorem

    def update(self):
        self.get_keys()
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.velocity * self.game.dt
        self.hit_box.centerx = self.position.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_box.centery = self.position.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_box.center

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_image
        self.rect = self.image.get_rect()
        self.hit_box = MOB_HIT_BOX.copy()
        self.hit_box.center = self.rect.center
        self.position = vec(x, y) * TILESIZE
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.rect.center = self.position
        self.rotation = 0

    def update(self):
        self.rotation = (self.game.player.position - self.position).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.acceleration = vec(MOB_SPEED, 0).rotate(-self.rotation)
        self.acceleration += self.velocity * -1  # applies friction to the mob movement
        self.velocity += self.acceleration * self.game.dt
        self.position += (self.velocity * self.game.dt) + (0.5 * self.acceleration * self.game.dt ** 2)
        self.rect.centerx = self.position.x
        collide_with_walls(self, self.game.walls, "x")
        self.rect.centery = self.position.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_box.center
