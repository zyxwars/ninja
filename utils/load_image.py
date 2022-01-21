import pygame as pg

from .get_path import get_path


def load_image(rel_path, script_path=None):
    if not script_path:
        return pg.image.load(rel_path).convert_alpha()
    return pg.image.load(get_path(script_path, rel_path)).convert_alpha()
