import pygame as pg


from level.tile import Tile
from utils import debug
import config


pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
# Load display surface after it is created
debug.init()
clock = pg.time.Clock()

level = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
tiles = pg.sprite.Group()
drag_start_pos = (0, 0)
zoom = 1


with open('./level/level.txt', encoding='utf-8') as f:
    for row_index, row in enumerate(f):
        for col_index, tile in enumerate(row):
            if tile in [' ', '', '\n']:
                continue
            else:
                tiles.add(Tile((col_index * config.TILE_SIZE,
                          row_index * config.TILE_SIZE), tile))


PALETTE_SIZE = 8 * (config.TILE_SIZE + 4) + 4
palette = pg.Surface((PALETTE_SIZE, config.SCREEN_HEIGHT))
tile_palette = pg.sprite.Group()
selected_tile_type = 0

x = 0
for i, tile_type in enumerate(['0', '1', '2', "3", "4", "5", "6", "7", "8", "9", 'P']):
    if i % 8 == 0:
        x = 0
    x += 4
    row = i // 8
    y = row * config.TILE_SIZE + 4 * (row + 1)
    tile_palette.add(
        Tile((x, y), tile_type))

    x += config.TILE_SIZE


while True:
    events = pg.event.get()
    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    for e in events:
        if e.type == pg.QUIT:
            pg.quit()

    # Level is in focus
    if mouse_pos[0] < config.SCREEN_WIDTH - PALETTE_SIZE:
        for e in events:
            # Zoom
            if e.type == pg.MOUSEWHEEL:
                zoom += e.y * 0.1
                if zoom < 0.1:
                    zoom = 0.1
                level = pg.Surface(
                    (config.SCREEN_WIDTH * zoom ** -1, config.SCREEN_HEIGHT * zoom ** -1))
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Start scroll
                if e.button == 1 and keys[pg.K_LCTRL]:
                    drag_start_pos = mouse_pos

        # Scroll level
        if keys[pg.K_LCTRL] and mouse[0]:
            for tile in tiles.sprites():
                tile.rect.x += mouse_pos[0] - drag_start_pos[0]
                tile.rect.y += mouse_pos[1] - drag_start_pos[1]

            drag_start_pos = mouse_pos

        # Delete tile
        if mouse[2]:
            for tile in tiles:
                mouse_pos = pg.mouse.get_pos()
                if tile.rect.collidepoint(mouse_pos[0] * zoom ** -1, mouse_pos[1] * zoom ** -1):
                    tiles.remove(tile)

        level.fill('gray')
        tiles.draw(level)

        level_size = level.get_size()
        scaled_level = pg.transform.scale(
            level, (level_size[0] * zoom, level_size[1] * zoom))
        screen.blit(scaled_level, (0, 0))
    # Palette is in focus
    else:
        pass

    # Palette gui should render even when not in focus
    palette.set_alpha(50)
    palette.fill('yellow')
    tile_palette.draw(palette)

    screen.blit(palette, (config.SCREEN_WIDTH - PALETTE_SIZE, 0))

    pg.display.update()
    clock.tick(60)
