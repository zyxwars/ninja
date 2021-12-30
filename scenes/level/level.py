import pygame as pg

from ..playable_scene import PlayableScene


class Level(PlayableScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
