import pygame as pg


class Debug():
    def __init__(self):
        pg.font.init()
        self.font_size = 24
        self.font = pg.font.Font(None, self.font_size)
        self.surface = pg.display.get_surface()
        self.tracked_dict = {}

    def init(self):
        self.surface = pg.display.get_surface()

    def debug(self, key, value):
        self.tracked_dict[key] = value

    def draw(self):
        for i, tracked_item in enumerate(self.tracked_dict.items()):
            debug_text = self.font.render(
                f'{tracked_item[0]}: {tracked_item[1]}', True, 'black', 'white')
            debug_rect = debug_text.get_rect(
                topleft=(4, i * self.font_size + 4))

            self.surface.blit(debug_text, debug_rect)


# Singleton
debug = Debug()
