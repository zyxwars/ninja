import pygame as pg


from scenes.playable_scene import PlayableScene
import game
from utils import debug
from .level import Level


class Hub(PlayableScene):
    def __init__(self, change_level_cb, *args, **kwargs):
        self.change_level_cb = change_level_cb
        super().__init__(*args, **kwargs)

    def update(self, *args, **kwargs):
        for e in game.events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self.change_level_cb(Level('./scenes/level/1.csv'))

        debug.debug('press e to change level', '')

        super().update(*args, **kwargs)
