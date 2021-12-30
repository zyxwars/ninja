from typing import Tuple
import pygame as pg


class ShiftableSprite(pg.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, screen, shift: Tuple):
        screen.blit(self.image, (self.rect.x +
                    int(shift.x), self.rect.y + int(shift.y)))
