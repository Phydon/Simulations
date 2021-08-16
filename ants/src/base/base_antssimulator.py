import pygame as pg
import os
import random
from simulsettings_base import *


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
        if self.alive == 1:
            surface.blit(
                self.image, (position.x, position.y))

    def remove_obj(self, target_lst):
        del self.image
        self.position = pg.Rect(0, 0, 0, 0)
        target_lst.remove(self)
        self.alive = 0

    def check_collision(self, target, target_lst):
        if self.position.x == target.position.x and self.position.y == target.position.y:
            print('\nCollision detected')
            if target.alive:
                target.remove_obj(target_lst)
                print('Object removed')
                self.collision = 1
                return True
        return False


class Entity(Objects):
    def __init__(self, pheromone_colour,
                 imagefolder, image, settings):
        self.width = settings['entity_width']
        self.height = settings['entity_height']

        self.position = pg.Rect(
            random.choice([
                settings['home_x'] - settings['start_variance'],
                settings['home_x'] + settings['start_variance']]),
            random.choice([
                settings['home_y'] - settings['start_variance'] - 1,
                settings['home_y'] + settings['start_variance'] + 1]),
            settings['entity_width'],
            settings['entity_height'])

        self.pheromone = settings['pheromone']
        self.pheromone_colour = pheromone_colour

        # load and transform image
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['entity_width'], settings['entity_height']))
        self.rect = self.image.get_rect()

        # set live
        self.alive = 1

        # set collision variable
        self.collision = 0

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

    def return_home(self, settings):
        self.pheromone_path(self.position.x, self.position.y, settings)

        homex = settings['home_x']
        homey = settings['home_y']
        # bottom right
        if self.position.x > homex and self.position.y > homey:
            self.position.x -= settings['velocity']
            self.position.y -= settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # top right
        elif self.position.x > homex and self.position.y < homey:
            self.position.x -= settings['velocity']
            self.position.y += settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # top left
        elif self.position.x < homex and self.position.y < homey:
            self.position.x += settings['velocity']
            self.position.y += settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # bottom left
        elif self.position.x < homex and self.position.y > homey:
            self.position.x += settings['velocity']
            self.position.y -= settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # bottom
        elif self.position.x == homex and self.position.y > homey:
            self.position.y -= settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # top
        elif self.position.x == homex and self.position.y < homey:
            self.position.y += settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # right
        elif self.position.x > homex and self.position.y == homey:
            self.position.x -= settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # left
        elif self.position.x < homex and self.position.y == homey:
            self.position.x += settings['velocity']
            return self.position.x, self.position.y, self.pheromone
        # home
        elif self.position.x == homex and self.position.y == homey:
            self.collision = 0
            self.pheromone.clear()
            return self.collision, self.pheromone
        else:
            print('Something horrible happend')


class Food(Objects):
    def __init__(self, imagefolder, image):
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['food_width'], settings['food_height']))
        self.rect = self.image.get_rect()

        self.position = pg.Rect(
            random.choice([
                random.randrange(
                    100, settings['WIDTH'] // 2) - settings['food_position_x'],
                random.randrange(settings['WIDTH'] // 2, settings['WIDTH'] - 100) + settings['food_position_x']]),
            random.choice([
                random.randrange(
                    100, settings['HEIGHT'] // 2) - settings['food_position_y'],
                random.randrange(settings['HEIGHT'] // 2, settings['HEIGHT'] - 100) + settings['food_position_y']]),
            settings['food_width'],
            settings['food_height'])

        # set live
        self.alive = 1


class Home(Objects):
    def __init__(self, imagefolder, image):
        self.image = pg.transform.scale(pg.image.load(
            os.path.join(imagefolder, image)), (settings['home_width'], settings['home_height']))
        self.rect = self.image.get_rect()

        self.position = pg.Rect(
            settings['home_x'], settings['home_y'], settings['home_width'], settings['home_height'])

        # set live
        self.alive = 1


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

    meals = [Food(settings['ASSETS_PATH'], 'redgreenpixel.jpg')
             for _ in range(settings['number_food'])]

    home = Home(settings['ASSETS_PATH'], 'orangepixel.jpg')

    for ant in ants:
        ant.draw_obj(ant.position)

    for meal in meals:
        meal.draw_obj(meal.position)

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

        for meal in meals:
            meal.draw_obj(meal.position)

        home.draw_obj(home.position)

        for ant in ants:
            for meal in meals:
                found = ant.check_collision(meal, meals)
                if found:
                    print('returning home')
                    ant.draw_obj(ant.position)
                    ant.return_home(settings)
            if ant.collision == 1:
                ant.draw_obj(ant.position)
                ant.return_home(settings)
            else:
                ant.draw_obj(ant.position)
                ant.random_walk(ant.position, settings)

        if len(meals) == 0:
            for ant in ants:
                ant.draw_obj(ant.position)
                ant.return_home(settings)

        pg.display.update()

    print('Aborted')
    pg.time.wait(1000)
    pg.quit()


if __name__ == '__main__':
    print('Initializing ...')
    pg.init()

    # creating window and the name showing in the window title
    surface = pg.display.set_mode(
        (settings['WIDTH'], settings['HEIGHT']))
    pg.display.set_caption('Simulation')

    # main
    simulation(settings)
