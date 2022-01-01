import pygame as pg

from utils import debug
import config
import game
from scenes.level.hub import Hub


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.scene = Hub(self.change_level, './scenes/level/hub.csv')

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

    def change_level(self, new_level):
        self.scene = new_level


game_loop = Game()
game_loop.run()
