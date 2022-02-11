import pygame as pg

from .weapon import CollectableWeapon
from utils import get_path


class Katana(CollectableWeapon):
    # Turns out loading the sounds in constructor, causes lag every time a new weapon is instantiated
    pg.mixer.init()
    s = []
    for sound_name in range(1, 14):
        sound = pg.mixer.Sound(
            get_path(__file__, f'assets/swishes/swish-{sound_name}.wav'))
        sound.set_volume(0.5)
        s.append(sound)
    sounds = s

    def __init__(self, pos=None, *args, **kwargs):
        super().__init__(100, 250, 'katana', pos=pos, *args, **kwargs)
