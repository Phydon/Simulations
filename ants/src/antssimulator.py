import pygame as pg
import os
import random
from simulsettings import *


# functions ---------------------------------------------------------------


def draw_window():  # displaying the window and the borders
    surface.fill(settings['DARKVIOLETT'])
    pg.draw.rect(surface, settings['WHITE'], settings['border_right'])
    pg.draw.rect(surface, settings['WHITE'], settings['border_top'])
    pg.draw.rect(surface, settings['WHITE'], settings['border_down'])
    pg.draw.rect(surface, settings['WHITE'], settings['border_left'])


# classes -----------------------------------------------------------------

class Objects():
    def draw_obj(self, position):
        surface.blit(
            self.image, (position.x, position.y))

    def check_collision(self, target):
        pass


class Entity(Objects):
    def __init__(self, pheromone_colour,
                 imagefolder, image, settings):
        self.width = settings['entity_width']
        self.height = settings['entity_height']

        self.position = pg.Rect(
            random.choice([
                300 - settings['start_variance'],
                300 + settings['start_variance']]),
            random.choice([
                300 - settings['start_variance'],
                300 + settings['start_variance']]),
            settings['entity_width'],
            settings['entity_height'])

        self.pheromone = settings['pheromone']
        self.pheromone_colour = pheromone_colour

        # load and transform image
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['entity_width'], settings['entity_height']))
        self.rect = self.image.get_rect()

    def random_walk(self, position, settings):  # moving randomly
        num = random.randrange(4)

        # left
        if num == 0 and position.x - \
                settings['velocity'] > settings['border_left'].width:
            position.x -= settings['velocity']

        # right
        elif num == 1 and position.x + settings['velocity'] + position.width < settings['border_right'].left:
            position.x += settings['velocity']

        # up
        elif num == 2 and position.y - settings['velocity'] > settings['border_top'].height:
            position.y -= settings['velocity']

        # down
        elif num == 3 and position.y + settings['velocity'] + position.height < settings['border_down'].top:
            position.y += settings['velocity']

        else:
            pass

        return self.position

    def pheromone_path(self, positionx, positiony, settings):
        # draw path of entity
        self.pheromone.append((positionx, positiony))

        if len(self.pheromone) >= settings['pheromone_tail']:
            self.pheromone.pop(0)

        for i in range(len(self.pheromone)):
            pg.draw.rect(surface, self.pheromone_colour,
                         (self.pheromone[i], (1, 1)))

        return self.pheromone


class Food(Objects):
    def __init__(self, imagefolder, image):
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['food_width'], settings['food_height']))
        self.rect = self.image.get_rect()

        self.position = pg.Rect(
            random.choice([
                random.randrange(100, 250) - settings['food_position_x'],
                random.randrange(250, 400) + settings['food_position_x']]),
            random.choice([
                random.randrange(100, 250) - settings['food_position_y'],
                random.randrange(250, 400) + settings['food_position_y']]),
            settings['food_width'],
            settings['food_height'])


class Home(Objects):
    def __init__(self, imagefolder, image):
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['home_width'], settings['home_height']))
        self.rect = self.image.get_rect()

        self.position = pg.Rect(
            300 - settings['home_width'] // 2, 300 - settings['home_width'] // 2, settings['home_width'], settings['home_height'])


# main function -----------------------------------------------------------


def simulation(settings):

    # defining entities and objects
    print('Building Environment ...')

    ants = [Entity(
        settings['LIGHTRED'],
        settings['ASSETS_PATH'],
        'whitepixel.jpg',
        settings)
        for _ in range(settings['number_ants'])]

    meals = [Food(settings['ASSETS_PATH'], 'darkgreenpixel.jpg')
             for _ in range(settings['number_food'])]

    home = Home(settings['ASSETS_PATH'], 'orangepixel.jpg')

    # setting FPS and runnig simulation loop
    print('Simulation started')
    FramesPerSec = pg.time.Clock()
    run = True
    while run:
        FramesPerSec.tick(settings['fps'])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                print('Simulation aborted')
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    print('Simulation aborted')
                    pg.quit()

        draw_window()

        for ant in ants:
            ant.draw_obj(ant.position)
            ant.pheromone_path(
                ant.position.x,
                ant.position.y,
                settings)
            ant.random_walk(ant.position, settings)

        for meal in meals:
            meal.draw_obj(meal.position)
            # meal.check_collision(ant)

        home.draw_obj(home.position)

        pg.display.update()

    pg.time.wait(1000)
    pg.quit()


if __name__ == '__main__':
    pg.init()

    # creating window and the name showing in the window title
    print('Initializing ...')
    surface = pg.display.set_mode(
        (settings['WIDTH'], settings['HEIGHT']))
    pg.display.set_caption('Simulation')

    # main
    simulation(settings)
