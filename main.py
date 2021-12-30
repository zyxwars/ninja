import pygame as pg
import random

from scenes.level import Level
from utils import debug
import config
import game


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.scene = Level('./scenes/level/1.csv')

    def run(self):
        while True:
            # Call only once every frame
            game.events = pg.event.get()

            for e in game.events:
                if e.type == pg.QUIT:
                    pg.quit()

            if self.scene:
                self.scene.update(self.screen)

            debug.debug('delta_time', game.delta_time)
            debug.debug('fps', self.clock.get_fps())
            debug.draw(self.screen)

            pg.display.update()
            game.delta_time = self.clock.tick(300)


game_loop = Game()
game_loop.run()
