import json
import pygame as pg

from utils import debug

import game
from scenes.playable_scene import PlayableScene
from scenes.menus import Menu


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(
            (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.is_debug = False
        self.delta_time = 0
        self.events = []

        self.scene = Menu()

    def run(self):
        while True:
            # Call only once every frame
            self.events = pg.event.get()

            for e in self.events:
                if e.type == pg.QUIT:
                    pg.quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_F3:
                        self.is_debug = not self.is_debug

            if self.scene:
                self.scene.update(self.screen)

            debug.debug('delta_time', self.delta_time)
            debug.debug('fps', self.clock.get_fps())
            if self.is_debug:
                debug.draw(self.screen)

            pg.display.update()
            self.delta_time = self.clock.tick(300)

    def change_scene(self, new_level):
        self.scene = new_level

    def save_state(self, new_state):
        try:
            with open('state.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            data = {}

        data.update(new_state)

        with open('state.json', 'w') as f:
            json.dump(data, f)


game.loop = Game()

try:
    game.loop.run()
finally:
    pg.quit()
