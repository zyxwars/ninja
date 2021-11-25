import pygame as pg
from .get_path import get_path


class SpriteSheetParser:
    def __init__(self, script_path, relative_path):
        self.sheet = pg.image.load(
            get_path(script_path, relative_path)).convert_alpha()

    # Pos comprises of (column, row)
    def load_image(self, pos, scale=None, size=(32, 32)):
        image = pg.Surface(size, pg.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0),
                   (pos[0] * size[0], pos[1] * size[1], pos[0] * size[0] + size[0], pos[1] * size[1] + size[1]))
        if scale:
            image = pg.transform.scale(image, scale)
        return image

    def load_row(self, start_pos, num_of_images, scale=None, size=(32, 32)):
        images = []
        for i in range(num_of_images):
            image = self.load_image(
                (start_pos[0] + i, start_pos[1]), scale, size)
            images.append(image)

        return images
