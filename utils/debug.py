from typing import Any, Callable
import pygame as pg


class Debug():
    def __init__(self):
        pg.font.init()
        self.font_size = 24
        self.font = pg.font.Font(None, self.font_size)
        self.tracked_dict = {}
        self.debug_funcs = []
        self.debug_rects = []

    def debug(self, key, value):
        self.tracked_dict[key] = value

    def debug_func(self, cb:  Callable[[pg.Surface, dict], Any]):
        self.debug_funcs.append(cb)

    def debug_rect(self, rect, rect_color, is_shifted=True):
        if is_shifted:
            rect_copy = rect.copy()
            rect_copy.x += self.tracked_dict['shift'].x
            rect_copy.y += self.tracked_dict['shift'].y
            return self.debug_rects.append([rect_copy, rect_color])

        self.debug_rects.append([rect, rect_color])

    def draw(self, surface):
        for i, tracked_item in enumerate(self.tracked_dict.items()):
            debug_text = self.font.render(
                f'{tracked_item[0]}: {tracked_item[1]}', True, 'black', 'white')
            debug_rect = debug_text.get_rect(
                topleft=(4, i * self.font_size + 4))

            surface.blit(debug_text, debug_rect)

        for func in self.debug_funcs:
            func(surface)

        for rect in [*self.debug_rects]:
            pg.draw.rect(surface, rect[1], rect[0], 1)
            self.debug_rects.remove(rect)


# Singleton
debug = Debug()
