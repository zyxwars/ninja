import pygame as pg

from .weapon import Weapon
from utils import get_path


class Punch(Weapon):
    pg.mixer.init()
    s = []
    for sound_name in range(1, 38):
        sound = pg.mixer.Sound(
            get_path(__file__, f'assets/hits/hit{sound_name:02d}.mp3.flac'))
        sound.set_volume(0.5)
        s.append(sound)
    sounds = s

    def __init__(self, *args, **kwargs):
        super().__init__(25, 250, 'punch', *args, **kwargs)
