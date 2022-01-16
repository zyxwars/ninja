import pygame as pg

from .weapon import Weapon


class Punch(Weapon):
    def __init__(self,  *args, **kwargs):
        super().__init__(25, 250, 'punch', *args, **kwargs)
