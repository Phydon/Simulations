import pygame as pg
import os
from simulsettings import *
from entities import *


# functions ----------------------------------------------


def load_image(folder, file, background=0):
    file = os.path.join(folder, file)
    if not background:
        try:
            surface = pg.image.load(file)
        except pg.error:
            raise SystemExit(
                'Could not load image "&s" %s' %
                (file, pg.get_error()))
        return surface.convert()
    else:
        try:
            surface = pg.image.load(file)
        except pg.error:
            raise SystemExit(
                'Could not load image "%s" %s' %
                (file, pg.get_error()))
        return surface.convert()


def main(settings, winstyle=0):
    # initialize simulation
    print('Initializing ...')
    pg.init()

    fullscreen = False
    # set display mode
    winstyle = 0  # FULLSCREEN
    bestdepth = pg.display.mode_ok(settings['SCREENRECT'].size, winstyle, 32)
    screen = pg.display.set_mode(
        settings['SCREENRECT'].size, winstyle, bestdepth)

    # load images, assign to sprite class

    ant = pg.transform.scale(
        load_image(
            settings['ASSETS_PATH'],
            'whitepixel.jpg'),
        (settings['entity_width'],
         settings['entity_height']))
    Entity.images = [ant]
    meal = pg.transform.scale(
        load_image(
            settings['ASSETS_PATH'],
            'darkgreenpixel.jpg'),
        (settings['food_width'],
         settings['food_height']))
    Food.images = [meal]

    # decorate window
    pg.display.set_caption('Simulation')

    # create background
    background_tile = load_image(
        settings['ASSETS_PATH'],
        'background2.jpg',
        background=1)
    background = pg.Surface(settings['SCREENRECT'].size)
    for x in range(0, settings['SCREENRECT'].width,
                   background_tile.get_width()):
        background.blit(background_tile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    # initialize groups
    Ants = pg.sprite.Group()
    Meals = pg.sprite.Group()
    All = pg.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Entity.containers = Ants, All
    Food.containers = Meals, All

    # initialize starting sprites
    ants = [Entity(settings['WHITE'], settings)
            for _ in range(settings['number_ants'])]
    for ant in ants:
        ant

    meal = Food()

    # starting values
    print('Simulation started')
    FramesPerSec = pg.time.Clock()
    run = True

    # start simulation loop
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                print('Simulation aborted')
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    print('Simulation aborted')
                    pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            settings['SCREENRECT'].size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            settings['SCREENRECT'].size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        # clear/erase the last drawn sprites
        # all.clear(screen, background)

        # update all sprites
        all.update(settings)

        # check collision
        # for ant in pg.sprite.spritecollide(meal, ants, 1):
        #     meal.kill()

        # draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)

        # set framerate
        FramesPerSec.tick(settings['fps'])

    pg.time.wait(1000)
    pg.quit()


if __name__ == '__main__':
    main(settings)
