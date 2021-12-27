import pygame as pg

from level.level import Level
from utils import debug
import config
import game

pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()
level = Level(screen)


while True:
    # Call only once every frame
    game.events = pg.event.get()

    for e in game.events:
        if e.type == pg.QUIT:
            pg.quit()

    level.update()

    debug.debug('delta_time', game.delta_time)
    debug.debug('fps', clock.get_fps())
    debug.draw(screen)

    pg.display.update()
    game.delta_time = clock.tick(300)
