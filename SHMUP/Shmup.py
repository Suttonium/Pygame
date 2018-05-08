# Shmup
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import random
import pygame
from os import path

image_directory = path.join(path.dirname(__file__), "Images")
sound_directory = path.join(path.dirname(__file__), "Sounds")

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POWERUP_TIME = 5000


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot_time = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power > 1 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        # returns a list of every key that is currently pressed down
        keystate = pygame.key.get_pressed()
        if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and player.alive():
            self.speedx = -5
        if (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and player.alive():
            self.speedx = 5
        if keystate[pygame.K_SPACE] and player.alive():
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet_1 = Bullet(self.rect.left, self.rect.centery)
                bullet_2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet_1, bullet_2)
                bullets.add(bullet_1, bullet_2)
                shoot_sound.play()
            if self.power > 2:
                bullet_1 = Bullet(self.rect.left, self.rect.centery)
                bullet_2 = Bullet(self.rect.right, self.rect.centery)
                bullet_3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet_1, bullet_2, bullet_3)
                bullets.add(bullet_1, bullet_2, bullet_3)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)  # puts it off screen

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.rect = self.image_orig.get_rect()
        self.image = self.image_orig.copy()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)
        self.speed_x = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.time_last_updated = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_updated > 50:
            self.time_last_updated = current_time
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # kill it if it moves off screen
        if self.rect.bottom < 0:
            # deletes and removes bullet from game and/ or group  its in
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animations[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animations[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animations[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 3.5

    def update(self):
        self.rect.y += self.speed_y
        # kill it if it moves off screen
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def new_mob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


def draw_shield_bar(surface, x, y, shield_value):
    if shield_value < 0:
        shield_value = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill_percentage = (shield_value / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    filled_rect = pygame.Rect(x, y, fill_percentage, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, filled_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def draw_lives(surface, x, y, lives, imag):
    for j in range(lives):
        imag_rect = imag.get_rect()
        imag_rect.x = x + 30 * j
        imag_rect.y = y
        surface.blit(imag, imag_rect)


def show_game_over_screen():
    draw_text(game_display, "SHMUP", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(game_display, "Arrow keys or WASD to move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(game_display, "Press a key to begin", 18, WIDTH / 2, HEIGHT + 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if _event.type == pygame.KEYUP:
                waiting = False

# initialize pygame
pygame.init()
pygame.mixer.init()  # initializes sound

# create window
game_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)
pygame.display.set_caption("SHMUP")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")

# load all game graphics
background = pygame.image.load(path.join(image_directory, "bHiPMju.png")).convert()
background_rect = background.get_rect()

player_image = pygame.image.load(path.join(image_directory, "playerShip2_orange.png")).convert()
player_mini_image = pygame.transform.scale(player_image, (25, 19))
player_mini_image.set_colorkey(BLACK)
meteor_image = pygame.image.load(path.join(image_directory, "meteorBrown_med1.png")).convert()
bullet_image = pygame.image.load(path.join(image_directory, "laserRed01.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png",
               "meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small2.png",
               "meteorBrown_tiny1.png", "meteorBrown_tiny2.png"]
for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(image_directory, image)).convert())

explosion_animations = {"large": [], "small": [], "player": []}
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    image = pygame.image.load(path.join(image_directory, filename)).convert()
    image.set_colorkey(BLACK)
    large_image = pygame.transform.scale(image, (75, 75))
    explosion_animations["large"].append(large_image)
    small_image = pygame.transform.scale(image, (32, 32))
    explosion_animations["small"].append(small_image)
    file_name = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(image_directory, file_name)).convert()
    img.set_colorkey(BLACK)
    explosion_animations["player"].append(img)

powerup_images = {"shield": pygame.image.load(path.join(image_directory, "shield_gold.png")).convert(),
                  "gun": pygame.image.load(path.join(image_directory, "bolt_gold.png")).convert()}

# load game sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_directory, "Laser_Shoot3.wav"))
explosion_sounds = []
for sound in ["Explosion4.wav", "Explosion8.wav"]:
    explosion_sounds.append(pygame.mixer.Sound(path.join(sound_directory, sound)))
pygame.mixer.music.load(path.join(sound_directory, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)

shield_sound = pygame.mixer.Sound(path.join(sound_directory, "Randomize3.wav"))
power_sound = pygame.mixer.Sound(path.join(sound_directory, "Powerup.wav"))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    new_mob()

all_sprites.add(mobs)

# Game loop
score = 0
pygame.mixer.music.play(loops=-1)  # keep repeating the song
game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_mob()
        score = 0
    # keep this running at the right speed
    clock.tick(FPS)
    # process input/ events
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # check to see if mob hit the player
    # parameters = (sprite to check, group to check if hit sprite, whether sprite is deleted or not)
    # returns a list of collisions
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    # (True, True) deletes both the mobs and bullets when impact occurs
    bullet_hits_mobs = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in bullet_hits_mobs:
        score += 50 - hit.radius
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, "large")
        all_sprites.add(explosion)
        if random.random() > 0.9:
            power = Powerup(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        new_mob()
    # if list is empty (False), nothing happens.
    # if list isn't empty (True), game is over
    for hit in hits:
        player.shield -= hit.radius * 2
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, "small")
        all_sprites.add(explosion)
        new_mob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    powerup_hits_ship = pygame.sprite.spritecollide(player, powerups, True)
    for hit in powerup_hits_ship:
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "gun":
            power_sound.play()
            player.powerup()

    # if player died and explosion finished
    # noinspection PyUnboundLocalVariable
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # draw/ render
    game_display.blit(background, background_rect)
    all_sprites.draw(game_display)
    draw_text(game_display, str(score), 18, WIDTH / 2, 10)
    # noinspection PyTypeChecker
    draw_shield_bar(game_display, 5, 5, player.shield)
    draw_lives(game_display, WIDTH - 100, 5, player.lives, player_mini_image)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
quit()
