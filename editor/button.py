from typing import Callable
import pygame as pg

import game


class Button(pg.Surface):
    def __init__(self, text, on_click: Callable, size: tuple, pos: tuple, font_size=32, fg='white', bg='black', * args, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.fill(bg)
        self.rect = self.get_rect(topleft=pos)
        self.text = pg.font.Font(None, font_size).render(text, True, fg,)
        self.text_rect = self.text.get_rect()
        self.on_click = on_click

    def draw(self, surface):
        for e in game.events:
            if e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    if self.rect.collidepoint(e.pos):
                        self.on_click()
                        break

        self.blit(self.text, self.text_rect)
        surface.blit(self, self.rect)
