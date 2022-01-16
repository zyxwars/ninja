import pygame as pg

from .weapon import Weapon
from utils import get_path


class Katana(Weapon):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(100, 500, 'katana', pos, *args, **kwargs)
