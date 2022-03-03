import pygame as pg

import game


class Button:
    def __init__(self, size, pos, text='', on_click=lambda: None, fg='white', bg='black', font_size=24):
        self.font = pg.font.Font(None, font_size)
        self.image = pg.Surface(size)
        self.image.fill(bg)
        self.rect = self.image.get_rect(center=pos)
        self.text_surf = self.font.render(text, True, fg)
        self.text_rect = self.text_surf.get_rect(center=(pos))
        self.on_click = on_click
        self.light_up_by = 25

    def draw(self, screen):
        mouse = pg.mouse.get_pos()

        color = self.image.get_at((0, 0))
        if self.rect.collidepoint(*mouse):
            for e in game.loop.events:
                if e.type == pg.MOUSEBUTTONUP:
                    if e.button == 1:
                        return self.on_click()

            self.image.fill(
                (color[0] + self.light_up_by, color[1] + self.light_up_by, color[2] + self.light_up_by))

        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)

        self.image.fill(color)
