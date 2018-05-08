from PYTHON_MODULES.PYGAME.SI.bullet import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.transform.scale(game.player_image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot_time = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and self.alive():
            self.speedx = -5
        if (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and self.alive():
            self.speedx = 5
        if (keystate[pygame.K_SPACE]) and self.alive():
            self.shoot()

        # win condition for dying
        if self.lives < 0:
            self.game.show_screen("over")

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            self.bullet = Bullet(self.game, self.rect.centerx, self.rect.top, -10, "player")
            self.game.bullets.add(self.bullet)
            self.game.all_sprites.add(self.game.bullets)
            self.game.shoot_sound.play()
