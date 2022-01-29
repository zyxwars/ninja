import pygame as pg

from .weapon import CollectableWeapon
from utils import get_path


class Katana(CollectableWeapon):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(100, 500, 'katana', pos=pos, *args, **kwargs)
