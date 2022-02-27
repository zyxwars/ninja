import pygame as pg

from utils import debug
import config
import game
from scenes.playable_scene import PlayableScene
from scenes.menus import Menu


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.is_debug = False

        self.scene = Menu(self.change_scene)

    def run(self):
        while True:
            # Call only once every frame
            game.events = pg.event.get()

            for e in game.events:
                if e.type == pg.QUIT:
                    pg.quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_F3:
                        self.is_debug = not self.is_debug

            if self.scene:
                self.scene.update(self.screen)

            debug.debug('delta_time', game.delta_time)
            debug.debug('fps', self.clock.get_fps())
            if self.is_debug:
                debug.draw(self.screen)

            pg.display.update()
            game.delta_time = self.clock.tick(300)

    def change_scene(self, new_level):
        self.scene = new_level


game_loop = Game()
try:
    game_loop.run()
finally:
    pg.quit()
