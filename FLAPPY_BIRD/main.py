from os import path

from PYTHON_MODULES.PYGAME.FLAPPY_BIRD.sprites import *


class Game:
    """
    Create a new game object which loads the data and analyses the necessary events. It also updates, and draws
    the game as it runs.

    This basic constructor initializes pygame and sound. It also designates a resolution for the screen and
    creates the clock to track FPS. To end the constructor, the data for the game is loaded and the window icon is
    designated.
    """

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.playing = False
        self.load_data()
        pg.display.set_icon(self.icon)

    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, "Images")
        self.player_image = pg.image.load(path.join(image_folder, PLAYER_IMAGE)).convert_alpha()
        self.player_image = pg.transform.scale(self.player_image, (55, 45))
        self.background = pg.image.load(path.join(image_folder, BACKGROUND_IMAGE)).convert_alpha()
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.icon = pg.transform.scale(self.player_image, (30, 25))
        self.pipe_image = pg.image.load(path.join(image_folder, PIPE_IMAGE)).convert_alpha()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.bird = Bird(self, WIDTH / 2, HEIGHT / 2)
        self.pipes = pg.sprite.Group()
        self.top_pipes = pg.sprite.Group()
        self.bottom_pipes = pg.sprite.Group()

        self.top_pipes.add(Topipe(self, WIDTH, 0))
        self.bottom_pipes.add(Bottompipe(self, WIDTH, HEIGHT - 100))

        self.pipes.add(self.top_pipes)
        self.pipes.add(self.bottom_pipes)
        self.all_sprites.add(self.pipes)

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.show_pause_screen()

    def update(self):
        self.all_sprites.update()
        if self.bird.rect.centery >= HEIGHT:
            self.playing = False
            self.show_game_over_screen()
        hit = pg.sprite.spritecollide(self.bird, self.pipes, True)
        if hit:
            self.playing = False
            self.show_game_over_screen()

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    @staticmethod
    def draw_text(surface, text, size, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.draw_text(self.screen, "Flappy Bird", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Space To Jump, Don't Die!", 22, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to begin and P anytime to pause the game", 18, WIDTH / 2, HEIGHT - 50)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for _event in pg.event.get():
                if _event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if _event.type == pg.KEYUP:
                    self.playing = True
                    waiting = False

    def show_pause_screen(self):
        self.draw_text(self.screen, "PAUSED", 64, WIDTH / 2, HEIGHT / 5)
        self.draw_text(self.screen, "Press Any Key to Continue", 32, WIDTH / 2, HEIGHT - 50)
        pg.display.flip()
        paused = True
        while paused:
            self.clock.tick(FPS)
            for _event in pg.event.get():
                if _event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if _event.type == pg.KEYDOWN:
                    paused = False

    def show_game_over_screen(self):
        self.draw_text(self.screen, "GAME OVER", 128, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Press C to play again, Q to quit!", 32, WIDTH / 2, HEIGHT - 50)
        pg.display.flip()
        game_over = True
        while game_over:
            self.clock.tick(FPS)
            for _event in pg.event.get():
                if _event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if _event.type == pg.KEYDOWN:
                    if _event.key == pg.K_c:
                        game_over = False
                        self.playing = True
                        self.new()
                        self.run()
                    if _event.key == pg.K_q:
                        pg.quit()
                        quit()


def main():
    game = Game()
    game.show_start_screen()
    while game.playing:
        game.new()
        game.run()


if __name__ == "__main__":
    main()
