from PYTHON_MODULES.PYGAME.TILE.settings import *

def collide_hit_box(one, two):
    return one.hit_box.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())  # strips away any \n characters when read

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)  # calculates an offset because the map is moving in the opposite direction
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling
        x = min(0, x)  # left
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)
