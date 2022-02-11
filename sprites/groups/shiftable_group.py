from typing import Tuple
import pygame as pg


class ShiftableGroup(pg.sprite.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, screen, shift: pg.Vector2, invisible=[]):
        """invisible is used when draw is overwritten for specific sprites, so you don't draw them twice"""
        for sprite in self.sprites():
            if sprite in invisible:
                continue

            screen.blit(sprite.image, (sprite.rect.x +
                        int(shift.x), sprite.rect.y + int(shift.y)))
