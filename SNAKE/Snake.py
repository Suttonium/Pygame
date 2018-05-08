import pygame
import random

def game_over_screen():
    game_is_over = True

    while game_is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_is_over = False
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Game Over", black, -100, size="large")
        message_to_screen("Press C to Play Again or Q quit", black, 25)
        pygame.display.update()
        clock.tick(5)

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

def score(score_):
    text = small_font.render("Score: " + str(score_), True, black)
    game_display.blit(text, [0, 0])
    if score_ == 600:
        game_over_screen()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # X's out of the window
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False  # ends the entire method, starting the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Welcome to SNAKE", green, y_displace=-100, size="large")
        message_to_screen("The objective of the game is to eat red apples", black, y_displace=-30)
        message_to_screen("The more apples you eat, the longer you get", black, y_displace=10)
        message_to_screen("If you run into yourself, or the edges, you die", black, y_displace=50)
        message_to_screen("Press C to play or Q to quit", black, y_displace=180)
        message_to_screen("At any time you may press P to pause to game", black, y_displace=225, size="small")

        pygame.display.update()
        clock.tick(15)


def snake(size_of_block, snake_list):
    if direction == "right":
        head = pygame.transform.rotate(snake_image, 270)
        game_display.blit(head, [snake_list[-1][0], snake_list[-1][1]])
    if direction == "left":
        head = pygame.transform.rotate(snake_image, 90)
        game_display.blit(head, [snake_list[-1][0], snake_list[-1][1]])
    if direction == "up":
        head = snake_image
        game_display.blit(head, [snake_list[-1][0], snake_list[-1][1]])
    if direction == "down":
        head = pygame.transform.rotate(snake_image, 180)
        game_display.blit(head, [snake_list[-1][0], snake_list[-1][1]])

    for XnY in snake_list[:-1]:
        pygame.draw.rect(game_display, green, [XnY[0], XnY[1], size_of_block, size_of_block])


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

def rand_apple_gen(object_size):
    random_apple_x = round(random.randrange(0, display_width - object_size))  # / 10.0) * 10.0
    random_apple_y = round(random.randrange(0, display_height - object_size))  # / 10.0) * 10.0
    return random_apple_x, random_apple_y

def game_loop():
    global direction  # we can now alter the direction variable inside game_loop
    direction = "right"
    snake_list = []
    snake_length = 1
    game_exit = False
    game_over = False

    head_of_snake_x = display_width / 2
    head_of_snake_y = display_height / 2
    apple_thickness = 30

    head_of_snake_x_change = 10  # snake is already moving on game start
    head_of_snake_y_change = 0
    # rounding gives the apple a position on a multiple of 10 so the snake lines up with it
    random_apple_x, random_apple_y = rand_apple_gen(apple_thickness)

    while not game_exit:  # while game_exit is false
        while game_over:
            game_display.fill(white)
            message_to_screen("Game Over", red, y_displace=-50, size="large")
            message_to_screen("Press C to play again or Q to quit", black, y_displace=50, size="medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    head_of_snake_x_change = -block_size
                    head_of_snake_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    head_of_snake_x_change = block_size
                    head_of_snake_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_DOWN:
                    head_of_snake_y_change = block_size
                    head_of_snake_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_UP:
                    head_of_snake_y_change = -block_size
                    head_of_snake_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_p:
                    pause()

        if head_of_snake_x >= display_width or head_of_snake_x < 0 or head_of_snake_y >= display_height or head_of_snake_y < 0:
            game_over = True

        head_of_snake_x += head_of_snake_x_change
        head_of_snake_y += head_of_snake_y_change

        game_display.fill(white)  # fills the window with the created white color

        game_display.blit(apple_image, (random_apple_x, random_apple_y))
        # pygame.draw.rect(game_display, red, [random_apple_x, random_apple_y, apple_thickness, apple_thickness])
        # draws a rectangle on the game_display.
        # Its top left corner is positioned at 400,300 and it is 10 x 10

        snake_head = [head_of_snake_x, head_of_snake_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del (snake_list[0])

        for each_segment in snake_list[:-1]:  # anything up to the last element, -1 == last element
            if each_segment == snake_head:
                game_over = True

        snake(block_size, snake_list)
        score(snake_length - 1)
        pygame.display.update()  # updates the screen

        # if random_apple_x <= head_of_snake_x <= random_apple_x + apple_thickness:
        #     if random_apple_y <= head_of_snake_y <= random_apple_y + apple_thickness:
        #         random_apple_x = round(random.randrange(0, display_width - block_size))  # / 10.0) * 10.0
        #         random_apple_y = round(random.randrange(0, display_height - block_size))  # / 10.0) * 10.0
        #         snake_length += 1

        if random_apple_x < head_of_snake_x < random_apple_x + apple_thickness or random_apple_x < head_of_snake_x + block_size < random_apple_x + apple_thickness:
            if random_apple_y < head_of_snake_y < random_apple_y + apple_thickness:
                random_apple_x, random_apple_y = rand_apple_gen(apple_thickness)
                snake_length += 1
            elif random_apple_y < head_of_snake_y + block_size < random_apple_y + apple_thickness:
                random_apple_x, random_apple_y = rand_apple_gen(apple_thickness)
                snake_length += 1

        clock.tick(FPS)

    pygame.quit()  # uninitialised the game
    quit()  # closes the program


pygame.init()  # initializes the entire file

display_width = 800
display_height = 600

# initializes a color using its RGB values
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

# creates the surface/window for the game and makes its parameters 800 x 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("SNAKE")  # set the title

icon = pygame.image.load('Apple.png')
pygame.display.set_icon(icon)

snake_image = pygame.image.load('snake.png')
apple_image = pygame.image.load('Apple.png')

FPS = 15

direction = "right"

clock = pygame.time.Clock()
block_size = 20
small_font = pygame.font.SysFont("comicsansms", 25)
medium_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 75)

game_intro()
game_loop()
