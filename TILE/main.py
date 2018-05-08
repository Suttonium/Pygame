# Tile Based Game

from os import path

from PYGAME.TILE.tilemap import *

from PYTHON_MODULES.PYGAME.TILE.sprites import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.game_display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, "Images")
        self.map = Map(path.join(game_folder, "map.txt"))
        self.player_image = pg.image.load(path.join(image_folder, PLAYER_IMAGE)).convert_alpha()
        self.wall_image = pg.image.load(path.join(image_folder, WALL_IMG)).convert_alpha()
        self.wall_image = pg.transform.scale(self.wall_image, (TILESIZE, TILESIZE))
        self.mob_image = pg.image.load(path.join(image_folder, MOB_IMAGE)).convert_alpha()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    @staticmethod
    def quit():
        pg.quit()
        quit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.game_display, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.game_display, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.game_display.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.game_display.blit(sprite.image, self.camera.apply(sprite))
        # hit_box --> pg.draw.rect(self.game_display, WHITE, self.player.hit_box, 2)
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass


game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_game_over_screen()
