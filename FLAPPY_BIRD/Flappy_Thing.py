import pygame
import random


class Pipe:
    def __init__(self):
        self.width = 40
        self.space_between_pipes = 200
        self.top_height = random.randrange(display_height / 2)
        self.bottom_height = random.randrange(display_height / 2)
        if self.get_top_height() == self.get_bottom_height():
            self.bottom_height = random.randrange(display_height / 2)
        self.x_spawn = display_width

    def get_space_between_pipes(self):
        return self.space_between_pipes

    def get_width(self):
        return self.width

    def get_top_height(self):
        return self.top_height

    def get_bottom_height(self):
        return self.bottom_height

    def get_x_spawn(self):
        return self.x_spawn

    def draw(self):
        pygame.draw.rect(game_display, black, [self.get_x_spawn(), 0, self.get_width(), self.get_top_height()])
        pygame.draw.rect(game_display, black,
                         [self.get_x_spawn(), display_height - self.get_bottom_height(), self.get_width(),
                          self.get_bottom_height()])

    def move_x(self, delta):
        self.x_spawn -= delta


class Bird:
    def __init__(self):
        self.size = 15
        self.x_spawn = round(display_width / 2)
        self.y_spawn = round(display_height / 2)

    def draw(self):
        pygame.draw.circle(game_display, black, (self.get_x_spawn(), self.get_y_spawn()), self.get_size())

    def get_size(self):
        return self.size

    def get_x_spawn(self):
        return self.x_spawn

    def get_y_spawn(self):
        return self.y_spawn

    def move_y(self, delta):
        self.y_spawn += delta


def intro():
    intro_is_going = True

    while intro_is_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro_is_going = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Welcome to Flappy Thing", green, y_displace=-100, size="medium")
        message_to_screen("The objective of the game is to not die", black, y_displace=-30)
        message_to_screen("If you run into a barrier, you die", black, y_displace=50)
        message_to_screen("Press C to play or Q to quit", black, y_displace=180)
        message_to_screen("At any time you may press P to pause to game", black, y_displace=225, size="small")

        pygame.display.update()
        clock.tick(intro_FPS)


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Paused", black, -100, size="large")
        message_to_screen("Press C to Continue or Q quit", black, 25)
        pygame.display.update()
        clock.tick(5)


def current_score_is(score_):
    text = small_font.render("Score: " + str(score_), True, black)
    game_display.blit(text, [0, 0])


def text_objects(text, color, size):
    text_surface = "test"  # just added to avoid errors
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = medium_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):  # by default these parameters are set but you can adjust
    text_surface, text_rectangle = text_objects(msg, color, size)
    text_rectangle.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surface, text_rectangle)


def make_hero(radius, x_spawn, y_spawn):
    pygame.draw.circle(game_display, black, (x_spawn, y_spawn), radius)


def random_obstacle_height_generator():
    return round(random.randrange(0, maximum_obstacle_height))


def create_obstacles(pipe_list):
    for pipe in pipe_list:
        pipe.draw()

def hit(bird, pipe):
    if bird.get_y_spawn() < pipe.get_top_height() or bird.get_y_spawn() > display_height - pipe.get_bottom_height():
        if pipe.get_x_spawn() < bird.get_x_spawn() < pipe.get_x_spawn() + display_width:
            return True
        else:
            return False
    else:
        return False


def game_loop():
    running = True
    game_over = False

    obstacle_list = [Pipe()]
    bird = Bird()

    score = 0

    deletion_point = 25

    bird_ascending_variable = 25
    bird_descending_variable = 15

    obstacle_x_change = 5

    bird_y_change = 0

    frame_count = 0

    while running:
        while game_over:
            game_display.fill(white)
            message_to_screen("Game Over", red, y_displace=-50, size="large")
            message_to_screen("Press C to play again or Q to quit", black, y_displace=50, size="medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = -bird_ascending_variable
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    bird_y_change = bird_descending_variable

        bird.move_y(bird_y_change)

        if bird.get_y_spawn() >= display_height:
            bird_y_change = 0
            game_over = True

        game_display.fill(blue)

        bird.draw()

        if frame_count % 75 == 0:
            obstacle_list.append(Pipe())

        create_obstacles(obstacle_list)

        for pipe in obstacle_list:
            pipe.move_x(obstacle_x_change)
            if pipe.get_x_spawn() + pipe.get_width() == deletion_point:
                obstacle_list.remove(pipe)
            elif pipe.get_x_spawn() < bird.get_x_spawn() < pipe.get_x_spawn() + pipe.get_width():
                if hit(bird, pipe):
                    game_display.fill(red)

        current_score_is(str(score))
        frame_count += 1
        pygame.display.update()
        clock.tick(game_FPS)

    pygame.quit()
    quit()

pygame.init()

display_width = 800
display_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (220, 240, 255)

intro_FPS = 18
game_FPS = 30

clock = pygame.time.Clock()

game_display = pygame.display.set_mode((display_width, display_height), pygame.HWSURFACE)

pygame.display.set_caption("Flappy Thing...")

small_font = pygame.font.SysFont("comicsansms", 25)
medium_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 75)

maximum_obstacle_height = 500

intro()
game_loop()
