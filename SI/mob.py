import random

from PYTHON_MODULES.PYGAME.SI.bullet import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if y == self.game.initial_y_spawn:
            self.first_image = pygame.transform.scale(self.game.top_alien_image, (45, 35))
            self.second_image = pygame.transform.scale(self.game.top_alien_image_2, (45, 35))
            self.score = 100
        if y == self.game.initial_y_spawn + 50 or y == self.game.initial_y_spawn + 100:
            self.first_image = pygame.transform.scale(self.game.middle_alien_image, (45, 35))
            self.second_image = pygame.transform.scale(self.game.middle_alien_image_2, (45, 35))
            self.score = 50
        if y == self.game.initial_y_spawn + 150 or y == self.game.initial_y_spawn + 200:
            self.first_image = pygame.transform.scale(self.game.bottom_alien_image, (45, 35))
            self.second_image = pygame.transform.scale(self.game.bottom_alien_image_2, (45, 35))
            self.score = 10
        self.image = self.first_image
        self.image.set_colorkey(BLACK)
        self.second_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x_movement = 10
        self.time_last_updated = pygame.time.get_ticks()
        self.image_timer = pygame.time.get_ticks()
        self.chance_to_shoot = 0
        self.direction = "right"
        self.vertical = "nothing"

    def update(self):
        current_time = pygame.time.get_ticks()
        image_rotation = pygame.time.get_ticks()
        if current_time - self.time_last_updated > 250 and self.direction == "right":
            self.image = self.second_image
            if image_rotation - self.image_timer > 1000:
                self.image = self.first_image
                self.image_timer = image_rotation
            self.rect.centerx += self.x_movement
            if self.game.remaining_aliens < 10:
                self.chance_to_shoot = random.randint(0, 50)
            if 10 < self.game.remaining_aliens < 30:
                self.chance_to_shoot = random.randint(0, 75)
            if 31 < self.game.remaining_aliens < 51:
                self.chance_to_shoot = random.randint(0, 100)
            if self.chance_to_shoot == 1:
                self.shoot()
            self.time_last_updated = current_time
        if current_time - self.time_last_updated > 250 and self.direction == "left":
            self.image = self.second_image
            if image_rotation - self.image_timer > 1000:
                self.image = self.first_image
                self.image_timer = image_rotation
            self.rect.centerx -= self.x_movement
            if self.game.remaining_aliens < 10:
                self.chance_to_shoot = random.randint(0, 25)
            if 10 < self.game.remaining_aliens < 30:
                self.chance_to_shoot = random.randint(0, 50)
            if 31 < self.game.remaining_aliens < 51:
                self.chance_to_shoot = random.randint(0, 100)
            if self.chance_to_shoot == 1:
                self.shoot()
            self.time_last_updated = current_time

        if self.vertical == "go down":
            self.rect.centery += 1

        # win condition for aliens meeting a certain point
        if self.rect.bottom == self.game.player.rect.top:
            self.game.show_screen("over")

        self.vertical = "nothing"

    def shoot(self):
        self.bullet = Bullet(self.game, self.rect.centerx, self.rect.bottom, 7, "alien")
        self.game.mob_bullets.add(self.bullet)
        self.game.all_sprites.add(self.game.mob_bullets)
