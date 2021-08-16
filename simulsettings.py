import pygame as pg
from random import randrange


# setting environment variables -------------------------------------------
settings = {}

# paths
settings['ASSETS_PATH'] = 'simulations\\ants\\assets'

# (1000 is too big for 15,6'' screen)
settings['HEIGHT'] = 600                    # window height
settings['WIDTH'] = 600                     # window width

settings['SCREENRECT'] = pg.Rect(0, 0, settings['WIDTH'], settings['HEIGHT'])

# window border
settings['border_left'] = pg.Rect(
    0, 0, settings['WIDTH'] - (settings['WIDTH'] - 5), settings['HEIGHT'])

settings['border_right'] = pg.Rect(settings['WIDTH'] -
                                   5, 0, settings['WIDTH'] -
                                   (settings['WIDTH'] -
                                    5), settings['HEIGHT'])

settings['border_top'] = pg.Rect(
    0, 0, settings['WIDTH'], settings['HEIGHT'] - (settings['HEIGHT'] - 5))

settings['border_down'] = pg.Rect(0,
                                  settings['HEIGHT'] - 5,
                                  settings['WIDTH'],
                                  settings['HEIGHT'] - (settings['HEIGHT'] - 5))

settings['fps'] = 60                        # frames per second

# colours
settings['WHITE'] = (255, 255, 255)
settings['BLACK'] = (0, 0, 0)
settings['BLUE'] = (0, 0, 255)
settings['DARKVIOLETT'] = (25, 0, 51)
settings['VIOLETT'] = (51, 0, 102)
settings['RED'] = (255, 0, 0)
settings['LIGHTRED'] = (255, 51, 51)
settings['GREEN'] = (0, 255, 0)
settings['DARKGREEN'] = (51, 102, 0)
settings['PURPLE'] = (128, 0, 128)
settings['YELLOW'] = (255, 255, 0)
settings['ORANGE'] = (255, 165, 0)
settings['GREY'] = (50, 50, 50)
settings['TURQUOISE'] = (64, 224, 208)

# setting number of entities
settings['number_ants'] = 100
settings['number_food'] = 40

# setting properties
settings['entity_width'] = 3
settings['entity_height'] = 3
settings['pheromone'] = []                   # pheromone path
settings['pheromone_tail'] = 200             # pheromone tail length
settings['velocity'] = 1                     # step size of entity
settings['start_variance'] = 100             # variance of starting position

# setting food properties
settings['food_width'] = 5
settings['food_height'] = 5
settings['food_position_x'] = randrange(1, 150)
settings['food_position_y'] = randrange(1, 150)

# setting home properties
settings['home_width'] = 20
settings['home_height'] = 20
