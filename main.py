import pygame as pg

from level.level import Level

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

level = Level(screen)

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()

    screen.fill('gray')
    level.update()

    pg.display.update()
    clock.tick(60)
