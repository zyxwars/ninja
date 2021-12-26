import pygame as pg


from level.tile import Tile
from utils import debug
import config


pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()

level = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
tiles = pg.sprite.Group()
drag_start_pos = (0, 0)
zoom = 1


with open('./level/level.txt', encoding='utf-8') as f:
    for row_index, row in enumerate(f):
        for col_index, tile_type in enumerate(row):
            if tile_type in [' ', '', '\n']:
                continue
            else:
                tiles.add(Tile((col_index * config.TILE_SIZE,
                          row_index * config.TILE_SIZE), tile_type))


PALETTE_SIZE = 8 * (config.TILE_SIZE + 4) + 4
PALETTE_POS = config.SCREEN_WIDTH - PALETTE_SIZE
palette = pg.Surface((PALETTE_SIZE, config.SCREEN_HEIGHT))
palette_tiles = pg.sprite.Group()
palette_selected_tile = None

x = 0
for i, tile_type in enumerate(['0', '1', '2', "3", "4", "5", "6", "7", "8", "9", 'P']):
    if i % 8 == 0:
        x = 0
    x += 4
    row = i // 8
    y = row * config.TILE_SIZE + 4 * (row + 1)
    palette_tiles.add(
        Tile((x, y), tile_type))

    x += config.TILE_SIZE

# pg.mouse.set_visible(False)

while True:
    events = pg.event.get()
    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    for e in events:
        if e.type == pg.QUIT:
            pg.quit()

    # Level is in focus
    if mouse_pos[0] < PALETTE_POS:
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
        elif mouse[0] and palette_selected_tile:
            # Update existing tile texture
            for tile in tiles:
                if tile.rect.collidepoint(mouse_pos[0] * zoom ** -1, mouse_pos[1] * zoom ** -1):
                    tile.image = palette_selected_tile.image
                    tile.tile_type = palette_selected_tile.tile_type
                    break
            # Create new tile
            else:
                tile = Tile((mouse_pos[0] * zoom ** -1 // 32 * 32,
                            mouse_pos[1] * zoom ** -1 // 32 * 32), palette_selected_tile.tile_type)
                tiles.add(tile)

        # Delete tile
        if mouse[2]:
            for tile in tiles:
                if tile.rect.collidepoint(mouse_pos[0] * zoom ** -1, mouse_pos[1] * zoom ** -1):
                    tiles.remove(tile)
                    break

        level.fill('gray')
        tiles.draw(level)

        level_size = level.get_size()
        scaled_level = pg.transform.scale(
            level, (level_size[0] * zoom, level_size[1] * zoom))
        screen.blit(scaled_level, (0, 0))
    # Palette is in focus
    else:
        if mouse[0]:
            for i, tile in enumerate(palette_tiles):
                if tile.rect.collidepoint(mouse_pos[0] - PALETTE_POS, mouse_pos[1]):
                    palette_selected_tile = tile
                    break

    # Palette gui should render even when not in focus
    palette.set_alpha(50)
    palette.fill('white')
    palette_tiles.draw(palette)

    if palette_selected_tile:
        scaled_image = pg.transform.scale(
            palette_selected_tile.image, (config.TILE_SIZE * zoom, config.TILE_SIZE * zoom))
        screen.blit(scaled_image, mouse_pos)

    screen.blit(palette, (PALETTE_POS, 0))

    pg.display.update()
    clock.tick(60)
