from os import path

from PYTHON_MODULES.PYGAME.SI.mob import *
from PYTHON_MODULES.PYGAME.SI.player import *

from PYTHON_MODULES.PYGAME.SI.mystery import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.explosion_sounds = []
        self.score_blit_x = WIDTH - 15
        self.score_blit_y = HEIGHT - 20
        self.remaining_aliens = 50
        self.initial_x_spawn = 50
        self.initial_y_spawn = 75
        self.load_data()

    def load_data(self):
        self.directory = path.dirname(__file__)
        # load high score
        # 'r' allows the file to be read
        with open(path.join(self.directory, HS_FILE), 'r') as highscore_file:
            try:
                self.highscore = int(highscore_file.read())
            except:
                self.highscore = 0
        self.image_directory = path.join(self.directory, IMAGES)
        self.sound_directory = path.join(self.directory, SOUNDS)
        self.player_image = pygame.image.load(path.join(self.image_directory, PLAYER_IMAGE))
        self.mini_image = pygame.transform.scale(self.player_image, (25, 19))
        self.background = pygame.image.load(path.join(self.image_directory, BACKGROUND))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.top_alien_image = pygame.image.load(path.join(self.image_directory, TOP_MOB_IMAGE))
        self.top_alien_image_2 = pygame.image.load(path.join(self.image_directory, TOP_IMAGE_2))
        self.middle_alien_image = pygame.image.load(path.join(self.image_directory, MIDDLE_MOB_IMAGE))
        self.middle_alien_image_2 = pygame.image.load(
            path.join(self.image_directory, MIDDLE_MOB_IMAGE_2))
        self.bottom_alien_image = pygame.image.load(path.join(self.image_directory, BOTTOM_MOB_IMAGE))
        self.bottom_alien_image_2 = pygame.image.load(
            path.join(self.image_directory, BOTTOM_MOB_IMAGE_2))
        for sound in [EXPLOSION_1, EXPLOSION_2]:
            self.explosion_sounds.append(pygame.mixer.Sound(path.join(self.sound_directory, sound)))
        self.shoot_sound = pygame.mixer.Sound(path.join(self.sound_directory, LASER))
        self.mystery_spawn_sound = pygame.mixer.Sound(path.join(self.sound_directory, MYSTERY_SPAWN_SOUND))
        self.mystery_image = pygame.image.load(path.join(self.image_directory, MYSTERY)).convert()
        self.font = pygame.font.Font(None, 25)

    def new(self):
        self.score = 0
        self.mystery_counter = 0
        self.new_highscore = False
        # self.mystery = None
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mob_bullets = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.make_all_aliens()
        self.player = Player(self, WIDTH / 2, HEIGHT - 20)
        self.all_sprites.add(self.bullets)
        self.all_sprites.add(self.mob_bullets)
        self.all_sprites.add(self.mobs)
        self.initial_x_spawn = 50

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.show_screen("pause")

    def update(self):
        self.all_sprites.update()
        # mystery ship spawn
        if self.mystery_counter == 0:
            ship_spawn = random.randrange(0, 5000)
            if ship_spawn >= 4990:
                spawn_point = random.choice([0, 1])
                if spawn_point == 0:
                    self.mystery = Mystery(self, 0, 25, 2)
                else:
                    self.mystery = Mystery(self, WIDTH, 25, -2)
                self.mystery_counter += 1
                self.mystery_spawn_sound.play()

        if self.mystery_counter == 1:
            mystery_hits = pygame.sprite.spritecollide(self.mystery, self.bullets, True)
            if mystery_hits:
                self.mystery.kill()
                self.mystery_counter -= 1
                self.score += self.mystery.score
                random.choice(self.explosion_sounds).play(loops=-1)

        alien_bullet_hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, True)
        if alien_bullet_hits:
            random.choice(self.explosion_sounds).play()
            self.player.lives -= 1

        player_bullet_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in player_bullet_hits:
            self.score += hit.score
            self.remaining_aliens -= 1
            random.choice(self.explosion_sounds).play()

        for alien in self.mobs.sprites():
            if alien.rect.right >= WIDTH:
                for mob in self.mobs.sprites():
                    mob.direction = "left"
                    mob.vertical = "go down"
            if alien.rect.left <= 0:
                for mob in self.mobs.sprites():
                    mob.direction = "right"
                    mob.vertical = "go down"

        if self.remaining_aliens == 0:
            self.new_game_spawns()

        # update the text version of the score
        if self.score > self.highscore:
            self.new_highscore = True
            self.text = self.font.render("New Highscore: " + str(self.score), True, GREEN)
        else:
            self.text = self.font.render("Score: " + str(self.score), True, GREEN)

    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.background, self.background_rect)
        if not self.new_highscore:
            if len(str(self.score)) <= 2:
                self.score_blit_x = WIDTH - 75
            if len(str(self.score)) == 3:
                self.score_blit_x = WIDTH - 85
            if len(str(self.score)) > 3:
                self.score_blit_x = WIDTH - 95
        else:
            self.score_blit_x = WIDTH - 175
        self.screen.blit(self.text, [self.score_blit_x, self.score_blit_y])
        self.draw_lives(self.screen, 10, HEIGHT - 25, self.player.lives, self.mini_image)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    @staticmethod
    def draw_lives(screen, x, y, lives, image):
        for i in range(lives):
            imag_rect = image.get_rect()
            imag_rect.x = x + 30 * i
            imag_rect.y = y
            screen.blit(image, imag_rect)

    @staticmethod
    def draw_text(surface, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_screen(self, screen_to_show):
        waiting = True
        if screen_to_show == "start":
            self.draw_text(self.screen, "Space Invaders", 64, WIDTH / 2, HEIGHT / 4)
            self.draw_text(self.screen, "Space To Fire, Don't Die!", 22, WIDTH / 2, HEIGHT / 2)
            self.draw_text(self.screen, "Press a key to begin and P anytime to pause the game", 18, WIDTH / 2,
                           HEIGHT - 50)
            self.draw_text(self.screen, "Highscore: " + str(self.highscore), 22, WIDTH / 2, HEIGHT - 100)
            pygame.display.flip()
            while waiting:
                self.clock.tick(FPS)
                for _event in pygame.event.get():
                    if _event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if _event.type == pygame.KEYUP:
                        self.playing = True
                        waiting = False
        if screen_to_show == "over":
            self.draw_text(self.screen, "GAME OVER", 128, WIDTH / 2, HEIGHT / 4)
            self.draw_text(self.screen, "Press C to play again, Q to quit!", 32, WIDTH / 2, HEIGHT - 50)
            if self.score > self.highscore:
                self.highscore = self.score
                self.draw_text(self.screen, "NEW HIGH SCORE! " + str(self.highscore), 32, WIDTH / 2, HEIGHT - 100)
                # 'w' allows the file to be written to and will create the designated file if it does not exist
                with open(path.join(self.directory, HS_FILE), 'w') as highscore_file:
                    highscore_file.write(str(self.highscore))
            else:
                self.draw_text(self.screen, "Highscore: " + str(self.highscore), 22, WIDTH / 2, HEIGHT - 100)
            pygame.display.flip()
            while waiting:
                self.clock.tick(FPS)
                for _event in pygame.event.get():
                    if _event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if _event.type == pygame.KEYDOWN:
                        if _event.key == pygame.K_c:
                            waiting = False
                            self.playing = True
                            self.new()
                            self.run()
                        if _event.key == pygame.K_q:
                            pygame.quit()
                            quit()
        if screen_to_show == "pause":
            self.draw_text(self.screen, "PAUSED", 64, WIDTH / 2, HEIGHT / 5)
            self.draw_text(self.screen, "Press C to Continue or Q to Quit", 32, WIDTH / 2, HEIGHT - 50)
            pygame.display.flip()
            while waiting:
                self.clock.tick(FPS)
                for _event in pygame.event.get():
                    if _event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if _event.type == pygame.KEYDOWN:
                        if _event.key == pygame.K_c:
                            waiting = False
                        if _event.key == pygame.K_q:
                            pygame.quit()
                            quit()

    def new_game_spawns(self):
        self.make_all_aliens()
        self.all_sprites.add(self.mobs)
        self.remaining_aliens = 50
        self.initial_x_spawn = 50

    def make_all_aliens(self):
        for i in range(10):
            self.new_top_row_mob(self.initial_x_spawn, self.initial_y_spawn)
            self.new_second_row_mob(self.initial_x_spawn, self.initial_y_spawn + 50)
            self.new_third_row_mob(self.initial_x_spawn, self.initial_y_spawn + 100)
            self.new_fourth_row_mob(self.initial_x_spawn, self.initial_y_spawn + 150)
            self.new_fifth_row_mob(self.initial_x_spawn, self.initial_y_spawn + 200)
            self.initial_x_spawn += 55

    def new_top_row_mob(self, x_spawn, y_spawn):
        Mob(self, x_spawn, y_spawn)

    def new_second_row_mob(self, x_spawn, y_spawn):
        Mob(self, x_spawn, y_spawn)

    def new_third_row_mob(self, x_spawn, y_spawn):
        Mob(self, x_spawn, y_spawn)

    def new_fourth_row_mob(self, x_spawn, y_spawn):
        Mob(self, x_spawn, y_spawn)

    def new_fifth_row_mob(self, x_spawn, y_spawn):
        Mob(self, x_spawn, y_spawn)


def main():
    game = Game()
    game.show_screen("start")
    while game.playing:
        game.new()
        game.run()


if __name__ == "__main__":
    main()
