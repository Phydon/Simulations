import pygame
import os
import random


# setting environment variables
HEIGHT = 600  # window height (1000 is too big for 15,6'')
WIDTH = 600  # window width

FPS = 60  # frames per second

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# setting properties
velocity = 2

# creating window and the name showing in the window title
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulation')

# window border
border_left = pygame.Rect(0, 0, WIDTH - (WIDTH - 5), HEIGHT)
border_right = pygame.Rect(WIDTH - 5, 0, WIDTH - (WIDTH - 5), HEIGHT)
border_top = pygame.Rect(0, 0, WIDTH, HEIGHT - (HEIGHT - 5))
border_down = pygame.Rect(0, HEIGHT - 5, WIDTH, HEIGHT - (HEIGHT - 5))

"""
# tranforming the size of loaded images
ENTITY_WIDTH = 30
ENTITY_HEIGHT = 30

# load images
ENTITY_UNTRANSFORMED_IMAGE = pygame.image.load(
    os.path.join('Evolution Simulation\\Assets', 'rabbit_image.jpg'))
ENTITY_IMAGE = pygame.transform.scale(
    ENTITY_UNTRANSFORMED_IMAGE, (ENTITY_WIDTH, ENTITY_HEIGHT))
"""


class Entity():
    def __init__(self, velocity, pheromone_colour,
                 imagefolder, image, width, height):
        self.velocity = velocity
        self.pheromone_colour = pheromone_colour
        self.width = width
        self.height = height

        # load and transform image
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(imagefolder, image)), (width, height))

    def entity_movement(self, entity_position):  # random walk

        num = random.randrange(100)

        # left
        if num <= 25 and entity_position.x - velocity > border_left.width:
            entity_position.x -= velocity

        # right
        elif 25 < num <= 50 and entity_position.x + velocity + entity_position.width < border_right.left:
            entity_position.x += velocity

        # up
        elif 50 < num <= 75 and entity_position.y - velocity > border_top.height:
            entity_position.y -= velocity

        # down
        elif num > 75 and entity_position.y + velocity + entity_position.height < border_down.top:
            entity_position.y += velocity

        else:
            pass

        return entity_position

    def draw_entity(self, entity_position):  # draw entity and its path
        displaysurface.blit(
            self.image, (entity_position.x, entity_position.y))
        pheromone(
            displaysurface,
            self.pheromone_colour,
            entity_position.x,
            entity_position.y)
        pygame.display.update()


def pheromone(surface, pheromone_colour, x, y):  # draw path of entity
    pygame.draw.rect(surface, pheromone_colour, (x, y, 1, 1))


class Behavior():
    def __init__(self, name):
        self. name = name

    def search_food():
        pass

    def return_home():
        pass

    def escape():
        pass

    def hunt():
        pass


def draw_window():  # displaying the window and the borders
    displaysurface.fill(BLACK)
    pygame.draw.rect(displaysurface, WHITE, border_right)
    pygame.draw.rect(displaysurface, WHITE, border_top)
    pygame.draw.rect(displaysurface, WHITE, border_down)
    pygame.draw.rect(displaysurface, WHITE, border_left)
    pygame.display.update()


def simulation():  # main function -> setting FPS and runnig game loop

    # setting entities and defining their properties
    ant_size_x = 1
    ant_size_y = 1
    Ant = Entity(
        20,
        WHITE,
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        ant_size_x,
        ant_size_y)
    entity_position = pygame.Rect(150, 300, Ant.width, Ant.height)

    Ant2 = Entity(
        10,
        RED,
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        ant_size_x,
        ant_size_y)
    entity_position2 = pygame.Rect(450, 300, Ant2.width, Ant2.height)

    draw_window()

    FramesPerSec = pygame.time.Clock()
    run = True
    while run:
        FramesPerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        Ant.entity_movement(entity_position)
        Ant.draw_entity(entity_position)

        Ant2.entity_movement(entity_position2)
        Ant2.draw_entity(entity_position2)

    pygame.quit()


if __name__ == '__main__':
    simulation()
