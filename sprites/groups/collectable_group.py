import pygame as pg

from utils import outline

from .shiftable_group import ShiftableGroup
import game


class CollectableGroup(ShiftableGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_item = None
        # Gradually raise the highlighted item
        self.raise_by = 0

    def draw(self, player_rect, screen, shift: pg.Vector2):
        collectable_index = player_rect.collidelist(self.sprites())

        if collectable_index == -1:
            super().draw(screen, shift)
            self.raise_by = 0
            return

        item = self.sprites()[collectable_index]

        if not self.last_item == item:
            self.raise_by = 0

        large_item_image = pg.transform.scale2x(item.image)
        # Assure the item doesn't move down
        large_item_rect = large_item_image.get_rect(
            midbottom=(item.rect.midbottom[0], item.rect.midbottom[1]))

        screen.blit(large_item_image, (large_item_rect.x +
                                       int(shift.x), large_item_rect.y + int(shift.y) - min(self.raise_by, 10)))
        screen.blit(outline(large_item_image), (large_item_rect.x +
                                                int(shift.x), large_item_rect.y + int(shift.y) - min(self.raise_by, 10)))

        super().draw(screen, shift, invisible=[item])

        self.raise_by += game.loop.delta_time
        self.last_item = item
