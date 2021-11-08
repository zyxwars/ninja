import pygame as pg

from level.level import Level
from debug import debug
import config
import pygame_data

pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
# Load display surface after it is created
debug.init()
clock = pg.time.Clock()

level = Level(screen)


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()

    screen.fill('gray')
    level.update()

    debug.debug('delta_time', pygame_data.delta_time)
    debug.debug('fps', clock.get_fps())
    debug.update()
    pg.display.update()
    pygame_data.delta_time = clock.tick(144)
