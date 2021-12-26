import pygame as pg

from level.level import Level
from utils import debug
import config
import shared_data

pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()
level = Level(screen)


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()

    level.update()

    debug.debug('delta_time', shared_data.delta_time)
    debug.debug('fps', clock.get_fps())
    debug.draw(screen)

    pg.display.update()
    shared_data.delta_time = clock.tick(300)
