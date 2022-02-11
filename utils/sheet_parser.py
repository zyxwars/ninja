import pygame as pg
from .get_path import get_path
from .load_image import load_image


class SheetParser:
    def __init__(self, relative_path, file_path=None):
        self.sheet = load_image(relative_path, file_path)

    # Pos comprises of (column, row)

    def load_image(self, pos, size=(32, 32), scale=None):
        image = pg.Surface(size, pg.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0),
                   (pos[0] * size[0], pos[1] * size[1], pos[0] * size[0] + size[0], pos[1] * size[1] + size[1]))
        if scale:
            image = pg.transform.scale(image, scale)
        return image

    def load_images_row(self, start_pos, num_of_images, scale=None, size=(32, 32)):
        images = []
        for i in range(num_of_images):
            image = self.load_image(
                (start_pos[0] + i, start_pos[1]), size, scale)
            images.append(image)

        return images
