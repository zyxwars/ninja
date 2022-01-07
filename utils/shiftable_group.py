from typing import Tuple
import pygame as pg


class ShiftableGroup(pg.sprite.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, screen, shift: pg.Vector2):
        for sprite in self.sprites():
            screen.blit(sprite.image, (sprite.rect.x +
                        int(shift.x), sprite.rect.y + int(shift.y)))
