import csv
import pygame as pg

from level.tile import Tile
import config
from utils import filedialog, get_path
from utils import debug
from .button import Button
import game


PALETTE_SIZE = 8 * (config.TILE_SIZE + 4) + 4
PALETTE_POS_X = config.SCREEN_WIDTH - PALETTE_SIZE
HIDE_GRID_ZOOMOUT = 1
GRID_OPACITY = 30
# Grid background, colorkey filters out (1,2,3), so choose anything, but that
GRID_COLOR = 'white'
ENTITY_TYPES = ['player', 'checkpoint', 'finish']
TILE_TYPES = list(range(1, 64))


class Editor:
    def __init__(self):
        self.screen_surface = pg.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.level_surface = pg.Surface(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.tiles = pg.sprite.Group()
        self.is_fg_focus = True
        self.is_blend_fg_bg = False

        self.drag_start_pos = (0, 0)
        self.total_drag = pg.math.Vector2(0, 0)

        self.zoom = 1

        self.grid_surface = pg.Surface(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.grid_surface.set_alpha(GRID_OPACITY)

        pg.mouse.set_visible(False)
        self.cursors = {'normal': pg.image.load(get_path(__file__, 'assets/normal.png')), 'grab': pg.image.load(get_path(__file__, 'assets/grab.png')),
                        'eraser': pg.image.load(get_path(__file__, 'assets/eraser.png')), 'picker': pg.image.load(get_path(__file__, 'assets/picker.png'))}
        self.current_cursor = 'normal'
        self.toggle_cursors = ['picker']

        self.palette = pg.Surface((PALETTE_SIZE, config.SCREEN_HEIGHT))
        self.palette_tiles = pg.sprite.Group()
        self.palette_selected_tile = None
        self.load_palette()

        self.save_button = Button(
            'Save (f1)', self.save_level, (128, 32), (PALETTE_POS_X + 32, config.SCREEN_HEIGHT - 104), 32, 'white', 'red', pg.K_F1)
        self.load_button = Button(
            'Load (f2)', self.load_level, (128, 32), (PALETTE_POS_X + 32, config.SCREEN_HEIGHT - 64), 32, 'white', 'red', pg.K_F2)

        self.main()

    def load_level(self):
        filename = filedialog.askopenfilename()
        if not filename:
            return

        with open(filename, encoding='utf-8') as f:
            # Reset level
            self.tiles = pg.sprite.Group()
            self.total_drag = pg.math.Vector2(0, 0)

            reader = csv.reader(f, delimiter=',')

            for row_index, row in enumerate(reader):
                for col_index, tile_type in enumerate(row):
                    if tile_type.lstrip('+-').isdigit():
                        tile_type = int(tile_type)

                        if tile_type == 0:
                            continue

                    self.tiles.add(Tile((col_index * config.TILE_SIZE,
                                         row_index * config.TILE_SIZE), tile_type))

    def save_level(self):
        print('saving...')

        filename = filedialog.asksaveasfilename()
        if not filename:
            return

        # Without newline='' the file would have every second row empty
        with open(filename, 'w', newline='', encoding='utf-8') as f:
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

            writer = csv.writer(f, delimiter=",")
            for row in rows:
                largest_x = 0
                if len(row) > 0:
                    largest_x = max(row.keys())

                row_tile_types = (largest_x + 1) * [0]

                for tile_x, tile_type in row.items():
                    row_tile_types[tile_x] = tile_type

                writer.writerow(row_tile_types)

        print('saved')

    def load_palette(self):
        x = 0
        for i, tile_type in enumerate([*ENTITY_TYPES, *TILE_TYPES]):
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

        if mouse_pos[0] < PALETTE_POS_X:
            self.get_level_input()
        else:
            self.get_palette_input()

    def get_level_input(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        self.palette.set_alpha(int(255 / 2))

        debug.debug(
            'Draw (mouse 1) Grab (ctrl + mouse 1) Erase (mouse 2) Color picker (q)', self.current_cursor)
        debug.debug('Draw foreground (w)', self.is_fg_focus)
        debug.debug('Blend layers (z)', self.is_blend_fg_bg)

        for e in game.events:
            # Zoom
            if e.type == pg.MOUSEWHEEL:
                self.zoom += e.y * 0.1
                self.zoom = max(0.1, self.zoom)

                self.level_surface = pg.Surface(
                    (config.SCREEN_WIDTH * self.zoom ** -1, config.SCREEN_HEIGHT * self.zoom ** -1))
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Start scroll
                if e.button == 1 and keys[pg.K_LCTRL]:
                    self.drag_start_pos = mouse_pos
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_w:
                    self.is_fg_focus = not self.is_fg_focus
                if e.key == pg.K_z:
                    self.is_blend_fg_bg = not self.is_blend_fg_bg
                if e.key == pg.K_q:
                    self.current_cursor = 'normal' if self.current_cursor == 'picker' else 'picker'

        if mouse[0]:
            # Scroll level
            if keys[pg.K_LCTRL]:
                self.current_cursor = 'grab'

                drag = pg.math.Vector2(int((mouse_pos[0] - self.drag_start_pos[0]) * self.zoom ** -1), int(
                    (mouse_pos[1] - self.drag_start_pos[1]) * self.zoom ** -1))

                if self.total_drag.x + drag.x > 0:
                    drag.x = 0

                if self.total_drag.y + drag.y > 0:
                    drag.y = 0

                for tile in self.tiles.sprites():
                    tile.rect.x += drag.x
                    tile.rect.y += drag.y

                self.total_drag.x += drag.x
                self.total_drag.y += drag.y

                self.drag_start_pos = mouse_pos
            # Pick tile
            elif self.current_cursor == 'picker':
                for tile in self.tiles:
                    if tile.rect.collidepoint(mouse_pos[0] * self.zoom ** -1, mouse_pos[1] * self.zoom ** -1):
                        self.palette_selected_tile = tile
                        self.current_cursor = 'normal'
                        break
            # Draw tile
            elif self.palette_selected_tile:
                tile_type = self.palette_selected_tile.tile_type

                # If tile is string, that means it's entity, which is always in the foreground layer
                if not isinstance(tile_type, str):
                    if not self.is_fg_focus:
                        tile_type = -tile_type

                # Update existing tile texture
                for tile in self.tiles:
                    if tile.rect.collidepoint(mouse_pos[0] * self.zoom ** -1, mouse_pos[1] * self.zoom ** -1):
                        tile.image = self.palette_selected_tile.image.copy()
                        tile.set_type(
                            tile_type)
                        break
                # Create new tile
                else:

                    tile = Tile(((mouse_pos[0] * self.zoom ** -
                                1 - self.total_drag.x) // config.TILE_SIZE * config.TILE_SIZE + self.total_drag.x, (mouse_pos[1] * self.zoom ** -
                                                                                                                    1 - self.total_drag.y) // config.TILE_SIZE * config.TILE_SIZE + self.total_drag.y),
                                tile_type)
                    self.tiles.add(tile)
        # Delete tile
        elif mouse[2]:
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
                    self.current_cursor = 'normal'
                    break

    def draw(self):

        self.draw_level()
        self.draw_palette()
        self.draw_cursor()

        debug.draw(self.screen_surface)

    def draw_level(self):
        self.level_surface.fill('black')

        for tile in self.tiles.sprites():

            # String is entity, always in foreground
            if isinstance(tile.tile_type, str):
                continue

            if self.is_blend_fg_bg:
                tile.image.set_alpha(255)
                continue

            # Set bg opacity
            if tile.tile_type < 0:
                tile.image.set_alpha(
                    int(255 / (2 if self.is_fg_focus else 1)))
                continue

            # Set fg opacity
            tile.image.set_alpha(
                int(255 / (2 if not self.is_fg_focus else 1)))

        self.tiles.draw(self.level_surface)

        level_size = self.level_surface.get_size()
        scaled_level = pg.transform.scale(
            self.level_surface, (level_size[0] * self.zoom, level_size[1] * self.zoom))
        self.screen_surface.blit(scaled_level, (0, 0))

        if HIDE_GRID_ZOOMOUT > self.zoom:
            return

        self.grid_surface.fill((1, 2, 3))
        self.grid_surface.set_colorkey((1, 2, 3))
        for line in range(int(config.SCREEN_HEIGHT // (config.TILE_SIZE * self.zoom) + 1)):
            y = line * config.TILE_SIZE
            drag_shift = self.total_drag.y % config.TILE_SIZE
            pg.draw.line(self.grid_surface, GRID_COLOR, (0, (y + drag_shift) * self.zoom),
                         (config.SCREEN_WIDTH, (y + drag_shift) * self.zoom))

        for line in range(int(config.SCREEN_WIDTH // (config.TILE_SIZE * self.zoom) + 1)):
            x = line * config.TILE_SIZE
            drag_shift = self.total_drag.x % config.TILE_SIZE
            pg.draw.line(self.grid_surface, GRID_COLOR, ((x + drag_shift) * self.zoom, 0),
                         ((x + drag_shift) * self.zoom, config.SCREEN_HEIGHT))

        self.screen_surface.blit(self.grid_surface, (0, 0))

    def draw_palette(self):
        self.palette.fill('white')
        self.palette_tiles.draw(self.palette)

        self.screen_surface.blit(self.palette, (PALETTE_POS_X, 0))

        # This is on the main surface to keep it's alpha
        # If used on a different surface you would need to check against (mouse - surface offset)
        self.save_button.draw(self.screen_surface)
        self.load_button.draw(self.screen_surface)

    def draw_cursor(self):
        mouse_pos = pg.mouse.get_pos()

        # Non-scalable cursors, center in the top left corner
        if self.current_cursor == 'normal' and not self.palette_selected_tile or self.current_cursor in ['grab']:
            self.screen_surface.blit(
                self.cursors[self.current_cursor], (mouse_pos[0], mouse_pos[1]))
        # Scalable and centered cursors
        else:
            if self.current_cursor == 'normal' and self.palette_selected_tile:
                cursor = self.palette_selected_tile.image
            else:
                cursor = self.cursors[self.current_cursor]

            cursor = pg.transform.scale(
                cursor, (config.TILE_SIZE * self.zoom, config.TILE_SIZE * self.zoom))
            self.screen_surface.blit(
                cursor, (mouse_pos[0] - cursor.get_width() / 2, mouse_pos[1] - cursor.get_height() / 2))

    def main(self):
        while True:
            # Call only once every frame
            game.events = pg.event.get()

            if self.current_cursor not in self.toggle_cursors:
                self.current_cursor = 'normal'

            self.get_input()

            self.draw()

            pg.display.update()
            self.clock.tick(60)
