import pygame as pg

import config


class Debug():
    def __init__(self):
        pg.font.init()
        self.font_size = 24
        self.font = pg.font.Font(None, self.font_size)
        self.tracked_dict = {}
        self.debug_surface = pg.Surface(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pg.SRCALPHA)

    def debug(self, key, value):
        self.tracked_dict[key] = value

    def blit(self, surface, pos):
        self.debug_surface.blit(surface, pos)

    def draw(self, surface):
        for i, tracked_item in enumerate(self.tracked_dict.items()):
            debug_text = self.font.render(
                f'{tracked_item[0]}: {tracked_item[1]}', True, 'black', 'white')
            debug_rect = debug_text.get_rect(
                topleft=(4, i * self.font_size + 4))

            surface.blit(self.debug_surface, (0, 0))
            surface.blit(debug_text, debug_rect)


# Singleton
debug = Debug()
