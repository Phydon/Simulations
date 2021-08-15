import pygame
import os
import random


# setting environment variables -------------------------------------------
settings = {}

# (1000 is too big for 15,6'' screen)
settings['HEIGHT'] = 600                    # window height
settings['WIDTH'] = 600                     # window width

settings['FPS'] = 10                        # frames per second

# colours
settings['WHITE'] = (255, 255, 255)
settings['BLACK'] = (0, 0, 0)
settings['BLUE'] = (0, 0, 255)
settings['RED'] = (255, 0, 0)
settings['GREEN'] = (0, 255, 0)
settings['PURPLE'] = (128, 0, 128)
settings['YELLOW'] = (255, 255, 0)
settings['ORANGE'] = (255, 165, 0)
settings['GREY'] = (50, 50, 50)
settings['TURQUOISE'] = (64, 224, 208)

# setting number of entities
settings['N'] = 5

# setting properties
settings['entity_width'] = 2
settings['entity_height'] = 2
settings['pheromone'] = []                  # pheromone path
settings['pheromone_tail'] = 100            # pheromone tail length
settings['velocity'] = 5                    # step size of entity

# setting food properties
settings['food_width'] = 99
settings['food_height'] = 99
settings['food_position_x'] = 275
settings['food_position_y'] = 100


# window ------------------------------------------------------------------

# creating window and the name showing in the window title
displaysurface = pygame.display.set_mode(
    (settings['WIDTH'], settings['HEIGHT']))
pygame.display.set_caption('Simulation')

# window border
border_left = pygame.Rect(
    0, 0, settings['WIDTH'] - (settings['WIDTH'] - 5), settings['HEIGHT'])

border_right = pygame.Rect(settings['WIDTH'] -
                           5, 0, settings['WIDTH'] -
                           (settings['WIDTH'] -
                            5), settings['HEIGHT'])

border_top = pygame.Rect(
    0, 0, settings['WIDTH'], settings['HEIGHT'] - (settings['HEIGHT'] - 5))

border_down = pygame.Rect(0,
                          settings['HEIGHT'] - 5,
                          settings['WIDTH'],
                          settings['HEIGHT'] - (settings['HEIGHT'] - 5))

# functions ---------------------------------------------------------------


def check_collision(foodname, entity, food):
    FOOD_HIT = pygame.USEREVENT + 1

    if foodname.rect.colliderect(entity.rect):
        pygame.event.post(pygame.event.Event(FOOD_HIT))
        print('Collision')
        food = False  # remove food

        return food

    food = True

    return food


def draw_window():  # displaying the window and the borders
    displaysurface.fill(settings['GREY'])
    pygame.draw.rect(displaysurface, settings['WHITE'], border_right)
    pygame.draw.rect(displaysurface, settings['WHITE'], border_top)
    pygame.draw.rect(displaysurface, settings['WHITE'], border_down)
    pygame.draw.rect(displaysurface, settings['WHITE'], border_left)


# classes -----------------------------------------------------------------

class Entity():
    def __init__(self, entity_position, pheromone_colour,
                 imagefolder, image, settings):
        self.width = settings['entity_width']
        self.height = settings['entity_height']
        self.entity_position = entity_position
        self.pheromone_colour = pheromone_colour

        # load and transform image
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(imagefolder, image)), (settings['entity_width'], settings['entity_height']))
        self.rect = self.image.get_rect()

    def draw_entity(self, entity_position):
        displaysurface.blit(
            self.image, (entity_position.x, entity_position.y))

    def entity_movement(self, entity_position, settings):  # random walk
        num = random.randrange(100)

        # left
        if num <= 25 and entity_position.x - \
                settings['velocity'] > border_left.width:
            entity_position.x -= settings['velocity']

        # right
        elif 25 < num <= 50 and entity_position.x + settings['velocity'] + entity_position.width < border_right.left:
            entity_position.x += settings['velocity']

        # up
        elif 50 < num <= 75 and entity_position.y - settings['velocity'] > border_top.height:
            entity_position.y -= settings['velocity']

        # down
        elif num > 75 and entity_position.y + settings['velocity'] + entity_position.height < border_down.top:
            entity_position.y += settings['velocity']

        else:
            pass

        return entity_position

    def pheromone_path(self, positionx, positiony, settings):
        # draw path of entity
        settings['pheromone'].append((positionx, positiony))

        if len(settings['pheromone']) >= settings['pheromone_tail']:
            settings['pheromone'].pop(0)

        for i in range(len(settings['pheromone'])):
            pygame.draw.rect(displaysurface, self.pheromone_colour,
                             (settings['pheromone'][i], (1, 1)))

        return settings['pheromone']


class Food():
    def __init__(self, imagefolder, image):
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(imagefolder, image)), (settings['food_width'], settings['food_height']))
        self.rect = self.image.get_rect()

    # you need to create a variable 'food' inside the main function and set it
    # to 'True'

    def place_food(self, food, settings):
        if 1:
            displaysurface.blit(
                self.image, (settings['food_position_x'], settings['food_position_y']))
            food = True
            return food
        food = False
        return food

# main function -----------------------------------------------------------


def simulation(settings):
    # defining entities
    entity_position = pygame.Rect(
        300,
        300,
        settings['entity_width'],
        settings['entity_height'])

    """
    # create names for entites
    lst = [i for i in range(settings['N'])]
    names = []
    for num in lst:
        names.append(str(num))
    """

    objects = [Entity(
        entity_position,
        settings['YELLOW'],
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        settings)
        for _ in range(settings['N'])]

    """
    Ant = Entity(
        '0',
        entity_position,
        settings['YELLOW'],
        'simulations\\ants\\assets',
        'whitepixel.jpg',
        settings)
    """

    Meal = Food('simulations\\ants\\assets', 'orangepixel.jpg')

    # setting FPS and runnig simulation loop
    food = True
    FramesPerSec = pygame.time.Clock()
    run = True
    while run:
        FramesPerSec.tick(settings['FPS'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

        draw_window()

        for obj in objects:
            obj.draw_entity(entity_position)
            obj.entity_movement(entity_position, settings)
            obj.pheromone_path(entity_position.x, entity_position.y, settings)

        """
        Ant.draw_entity(entity_position)
        Ant.entity_movement(entity_position, settings)
        Ant.pheromone_path(entity_position.x, entity_position.y, settings)
        """

        # check_collision(Meal, Ant, food)
        Meal.place_food(food, settings)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    simulation(settings)
