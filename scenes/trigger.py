import pygame as pg


class Trigger(pg.rect.Rect):
    def __init__(self, on_trigger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_trigger = on_trigger

    def collidepoint(self, x, y):
        if super().collidepoint(x, y):
            self.on_trigger()
