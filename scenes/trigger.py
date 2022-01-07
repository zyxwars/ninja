import pygame as pg


class Trigger(pg.rect.Rect):
    def __init__(self, on_triggered, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_triggered = on_triggered

    def collidepoint(self, x, y):
        if super().collidepoint(x, y):
            self.on_triggered()
