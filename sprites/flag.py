import pygame as pg

from sprites.collectable import Collectable
from utils.load_image import load_image


class Flag(Collectable):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(load_image('flag.png', __file__), pos, *args, **kwargs)
