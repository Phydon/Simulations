import pygame
import os
import random


# setting environment variables
HEIGHT = 600  # window height (1000 is too big for 15,6'')
WIDTH = 600  # window width

FPS = 10  # frames per second

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (50, 50, 50)
TURQUOISE = (64, 224, 208)

# setting properties
pheromone = []
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
        if num <= 25 and entity_position.x - self.velocity > border_left.width:
            entity_position.x -= self.velocity

        # right
        elif 25 < num <= 50 and entity_position.x + self.velocity + entity_position.width < border_right.left:
            entity_position.x += self.velocity

        # up
        elif 50 < num <= 75 and entity_position.y - self.velocity > border_top.height:
            entity_position.y -= self.velocity

        # down
        elif num > 75 and entity_position.y + self.velocity + entity_position.height < border_down.top:
            entity_position.y += self.velocity

        else:
            pass

        return entity_position

    # define safezone / searchzone for entities

    def zone(self, posx, posy, zonex=15, zoney=15):
        pygame.draw.rect(displaysurface, ORANGE,
                         (posx, posy, zonex, zoney))


class Searcher(Entity):
    def search_food(self, searcher, food):
        # search food, if food found -> move to food
        FOOD_HIT = pygame.USEREVENT + 1

        if searcher.colliderect(food):
            pygame.event.post(pygame.event.Event(FOOD_HIT))
            food = False  # remove food
            # searcher should return home

    def return_home(self):
        pass

    def escape(self):
        # if hunter enters safezone -> escape in opposite direction
        pass


class Hunter(Entity):
    def hunt(self, hunter, quarry):
        # search quarry, if quarry found -> follow till catched
        QUARRY_HIT = pygame.USEREVENT + 1

        if hunter.colliderect(quarry):
            pygame.event.post(pygame.event.Event(QUARRY_HIT))
            # something.remove(quarry)
            del(quarry)
            pygame.time.delay(500)


# draw path of entity
def pheromone_path(x, y, pheromone=[], pheromone_colour=PURPLE):
    # pygame.draw.rect(surface, pheromone_colour, (x, y, 1, 1))
    pheromone.append((x, y))

    if len(pheromone) >= 500:
        pheromone.pop(0)

    for i in range(len(pheromone)):
        pygame.draw.rect(displaysurface, pheromone_colour,
                         (pheromone[i], (1, 1)))

    return pheromone


def place_food(food):  # you need to create a variable 'food' inside the main function and set it to 'True'
    if 1:
        pygame.draw.rect(
            displaysurface,
            GREEN,
            (300, 100, 100, 100))
        return food == True

    return food == False


def draw_entity(entity_position, image, pheromone_colour):  # draw entity and its path
    displaysurface.blit(
        image, (entity_position.x, entity_position.y))
    pheromone_path(
        entity_position.x,
        entity_position.y,
        pheromone,
        pheromone_colour)
    pygame.display.update()


def draw_window(entity, pos, food):  # displaying the window and the borders
    displaysurface.fill(GREY)
    pygame.draw.rect(displaysurface, WHITE, border_right)
    pygame.draw.rect(displaysurface, WHITE, border_top)
    pygame.draw.rect(displaysurface, WHITE, border_down)
    pygame.draw.rect(displaysurface, WHITE, border_left)
    # placing food in world
    place_food(food)
    draw_entity(pos, entity.image, entity.pheromone_colour)
    entity.entity_movement(pos)
    pygame.display.update()


def simulation():  # main function -> setting FPS and runnig game loop

    # setting entities and defining their properties
    ant_size_x = 10
    ant_size_y = 10

    Ant = Searcher(
        20,
        WHITE,
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        ant_size_x,
        ant_size_y)
    entity_position = pygame.Rect(150, 300, Ant.width, Ant.height)

    Ant2 = Hunter(
        10,
        RED,
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        ant_size_x,
        ant_size_y)
    entity_position2 = pygame.Rect(450, 300, Ant2.width, Ant2.height)

    # simulation loop
    food = True
    FramesPerSec = pygame.time.Clock()
    run = True
    while run:
        FramesPerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

        # drawing the screen
        draw_window(Ant, entity_position, food)

        # creating entites and move them around
        # Ant.entity_movement(entity_position)
        # Ant.draw_entity(entity_position)
        # Ant.zone(entity_position.x, entity_position.y)
        """
        Ant2.entity_movement(entity_position2)
        Ant2.draw_entity(entity_position2)
        """


if __name__ == '__main__':
    pygame.init()
    simulation()
