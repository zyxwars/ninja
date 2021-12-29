import pygame as pg

from .level import Level
import utils


class Hub(Level):
    def __init__(self, *args, **kwargs):
        super().__init__(utils.get_path(__file__, 'level/hub.csv'), *args, **kwargs)

        self.music = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/liyan.mp3'))
        self.music.set_volume(0.5)
        self.music.play(-1)
