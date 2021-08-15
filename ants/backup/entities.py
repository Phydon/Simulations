import pygame as pg
import random
from simulsettings import *


class Entity(pg.sprite.Sprite):

    images = []
    position = pg.Rect(
        random.choice([
            300 - settings['start_variance'],
            300 + settings['start_variance']]),
        random.choice([
            300 - settings['start_variance'],
            300 + settings['start_variance']]),
        settings['entity_width'],
        settings['entity_height'])

    def __init__(self, pheromone_colour, settings):
        # call Sprite initializer
        pg.sprite.Sprite.__init__(self, self.containers)

        # handling image
        self.image = self.images[0]
        self.rect = self.image.get_rect(
            center=(self.position.x, self.position.y))

        # defining properties
        self.width = settings['entity_width']
        self.height = settings['entity_height']
        self.pheromone_colour = pheromone_colour

        self.pheromone = settings['pheromone']

    def random_walk(self, settings):
        num = random.randrange(100)

        # left
        if num <= 25 and self.position.x - \
                settings['velocity'] > settings['border_left'].width:
            self.position.x -= settings['velocity']

        # right
        elif 25 < num <= 50 and self.position.x + settings['velocity'] + self.position.width < settings['border_right'].left:
            self.position.x += settings['velocity']

        # up
        elif 50 < num <= 75 and self.position.y - settings['velocity'] > settings['border_top'].height:
            self.position.y -= settings['velocity']

        # down
        elif num > 75 and self.position.y + settings['velocity'] + self.position.height < settings['border_down'].top:
            self.position.y += settings['velocity']

        else:
            pass

        return self.position

    def update(self, settings):
        self.image = self.images[0]
        # self.rect.move_ip(0, settings['velocity'])
        # self.random_walk(self, settings)


class Food(pg.sprite.Sprite):

    images = []

    def __init__(self):
        # call Sprite initializer
        pg.sprite.Sprite.__init__(self, self.containers)

        # handling image
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(300, 100))

        # defining properties
        self.food = 0

    def update(self, settings):
        self.image = self.images[0]
        if self.food:
            self.kill()
