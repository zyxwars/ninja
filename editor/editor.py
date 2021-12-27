import pygame as pg
from pygame.constants import MOUSEBUTTONUP

from level.tile import Tile
import config
from utils import get_path
from utils import debug
from .button import Button
import game


PALETTE_SIZE = 8 * (config.TILE_SIZE + 4) + 4
PALETTE_POS_X = config.SCREEN_WIDTH - PALETTE_SIZE


class Editor:
    def __init__(self):
        self.screen = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.level = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.tiles = pg.sprite.Group()
        self.drag_start_pos = (0, 0)
        self.total_drag = pg.math.Vector2(0, 0)
        self.zoom = 1

        pg.mouse.set_visible(False)
        self.cursors = {'normal': pg.image.load(get_path(__file__, 'assets/normal.png')), 'grab': pg.image.load(get_path(__file__, 'assets/grab.png')),
                        'eraser': pg.image.load(get_path(__file__, 'assets/eraser.png')), 'picker': pg.image.load(get_path(__file__, 'assets/picker.png'))}
        self.current_cursor = 'normal'

        self.palette = pg.Surface((PALETTE_SIZE, config.SCREEN_HEIGHT))
        self.palette_tiles = pg.sprite.Group()
        self.palette_selected_tile = None
        self.draw_palette_tiles()

        self.load_button = Button(
            'Load', lambda: self.load_level('../level/level.txt'), (128, 32), (50, 50), 32, 'white', 'red')

        self.main()

    def load_level(self, relative_path: str):
        with open(get_path(__file__, relative_path), encoding='utf-8') as f:
            # Reset level
            self.tiles = pg.sprite.Group()
            self.total_drag = pg.math.Vector2(0, 0)

            for row_index, row in enumerate(f):
                for col_index, tile_type in enumerate(row):
                    if tile_type in [' ', '', '\n']:
                        continue
                    else:
                        self.tiles.add(Tile((col_index * config.TILE_SIZE,
                                            row_index * config.TILE_SIZE), tile_type))

    def save_level(self, ):
        with open('test.txt', 'w', encoding='utf-8') as f:
            tiles = self.tiles.sprites()
            largest_y = 0
            for tile in tiles:
                largest_y = max(largest_y, tile.rect.y)

            largest_y = int(
                (largest_y - self.total_drag.y) // 32)

            rows = []
            for row in range(largest_y + 1):
                rows.append({})

            for tile in tiles:
                rows[int((tile.rect.y - self.total_drag.y) // 32)
                     ][int((tile.rect.x - self.total_drag.x) // 32)] = tile.tile_type

            for row in rows:
                if len(row) < 1:
                    continue

                largest_x = max(row.keys())
                row_tile_types = (largest_x + 1) * [' ']

                for tile_x, tile_type in row.items():
                    row_tile_types[tile_x] = tile_type
                row_tile_types.append('\n')

                f.writelines(row_tile_types)

    def draw_palette_tiles(self):
        x = 0
        for i, tile_type in enumerate(['0', '1', '2', "3", "4", "5", "6", "7", "8", "9", 'P']):
            if i % 8 == 0:
                x = 0
            x += 4
            row = i // 8
            y = row * config.TILE_SIZE + 4 * (row + 1)
            self.palette_tiles.add(
                Tile((x, y), tile_type))

            x += config.TILE_SIZE

    def get_input(self):
        mouse_pos = pg.mouse.get_pos()

        for e in game.events:
            if e.type == pg.QUIT:
                pg.quit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                if e.key == pg.K_F1:
                    print('saving')

                    self.save_level()

                    print('saved')

        if mouse_pos[0] < PALETTE_POS_X:
            self.get_level_input()
        else:
            self.get_palette_input()

    def get_level_input(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        self.palette.set_alpha(50)

        for e in game.events:
            # Zoom
            if e.type == pg.MOUSEWHEEL:
                self.zoom += e.y * 0.1
                self.zoom = max(0.1, self.zoom)

                self.level = pg.Surface(
                    (config.SCREEN_WIDTH * self.zoom ** -1, config.SCREEN_HEIGHT * self.zoom ** -1))
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Start scroll
                if e.button == 1 and keys[pg.K_LCTRL]:
                    self.drag_start_pos = mouse_pos

        # Scroll level
        if keys[pg.K_LCTRL] and mouse[0]:
            self.current_cursor = 'grab'
            for tile in self.tiles.sprites():
                tile.rect.x += mouse_pos[0] - self.drag_start_pos[0]
                tile.rect.y += mouse_pos[1] - self.drag_start_pos[1]

            self.total_drag.x += mouse_pos[0] - self.drag_start_pos[0]
            self.total_drag.y += mouse_pos[1] - self.drag_start_pos[1]

            self.drag_start_pos = mouse_pos

        elif mouse[0] and self.palette_selected_tile:
            # Update existing tile texture
            for tile in self.tiles:
                if tile.rect.collidepoint(mouse_pos[0] * self.zoom ** -1, mouse_pos[1] * self.zoom ** -1):
                    tile.image = self.palette_selected_tile.image
                    tile.tile_type = self.palette_selected_tile.tile_type
                    break
            # Create new tile
            else:
                tile = Tile(((mouse_pos[0] * self.zoom ** -
                            1 - self.total_drag.x) // config.TILE_SIZE * config.TILE_SIZE + self.total_drag.x, (mouse_pos[1] * self.zoom ** -
                                                                                                                1 - self.total_drag.y) // config.TILE_SIZE * config.TILE_SIZE + self.total_drag.y),
                            self.palette_selected_tile.tile_type)
                self.tiles.add(tile)

        # Delete tile
        if mouse[2]:
            self.current_cursor = 'eraser'
            for tile in self.tiles:
                if tile.rect.collidepoint(mouse_pos[0] * self.zoom ** -1, mouse_pos[1] * self.zoom ** -1):
                    self.tiles.remove(tile)
                    break

    def get_palette_input(self):
        mouse = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        self.palette.set_alpha(255)

        if mouse[0]:
            for tile in self.palette_tiles:
                if tile.rect.collidepoint(mouse_pos[0] - PALETTE_POS_X, mouse_pos[1]):
                    self.palette_selected_tile = tile
                    break

    def draw(self):
        mouse_pos = pg.mouse.get_pos()

        # region render Level
        self.level.fill('gray')
        self.tiles.draw(self.level)
        level_size = self.level.get_size()
        scaled_level = pg.transform.scale(
            self.level, (level_size[0] * self.zoom, level_size[1] * self.zoom))
        self.screen.blit(scaled_level, (0, 0))
        # endregion

        # region render Palette
        self.palette.fill('white')
        self.palette_tiles.draw(self.palette)
        self.screen.blit(self.palette, (PALETTE_POS_X, 0))
        # endregion

        self.load_button.draw(self.screen)

        # region render Cursor
        # Non-scalable cursors, center in the top left corner
        if self.current_cursor == 'normal' and not self.palette_selected_tile or self.current_cursor in ['grab']:
            self.screen.blit(
                self.cursors[self.current_cursor], (mouse_pos[0], mouse_pos[1]))
        # Scalable and centered cursors
        else:
            if self.current_cursor == 'normal' and self.palette_selected_tile:
                cursor = self.palette_selected_tile.image
            else:
                cursor = self.cursors[self.current_cursor]

            cursor = pg.transform.scale(
                cursor, (config.TILE_SIZE * self.zoom, config.TILE_SIZE * self.zoom))
            self.screen.blit(
                cursor, (mouse_pos[0] - cursor.get_width() / 2, mouse_pos[1] - cursor.get_height() / 2))
        # endregion

        debug.draw(self.screen)

    def main(self):
        while True:
            # Call only once every frame
            game.events = pg.event.get()

            self.current_cursor = 'normal'

            self.get_input()

            self.draw()

            pg.display.update()
            self.clock.tick(60)
