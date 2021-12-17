import pygame as pg


from level.tile import Tile
from utils import debug
import config


pg.init()
screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
# Load display surface after it is created
debug.init()
clock = pg.time.Clock()

editor = pg.Surface((config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT))
tiles = pg.sprite.Group()
drag_start = (0, 0)
is_dragging = False
level = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
zoom = 1


with open('./level/level.txt', encoding='utf-8') as f:
    for row_index, row in enumerate(f):
        for col_index, tile in enumerate(row):
            if tile in [' ', '', '\n']:
                continue
            else:
                tiles.add(Tile((col_index * config.TILE_SIZE,
                          row_index * config.TILE_SIZE), tile))


while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
        elif e.type == pg.MOUSEWHEEL:
            zoom += e.y * 0.1
            if zoom <= 0:
                zoom = 0.1
            level = pg.Surface(
                (config.SCREEN_WIDTH * zoom ** -1, config.SCREEN_HEIGHT * zoom ** -1))
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                is_dragging = True
                drag_start = e.pos
        elif e.type == pg.MOUSEBUTTONUP:
            if e.button == 1:
                is_dragging = False

    editor.fill('gray')
    level.fill('gray')
    tiles.draw(level)

    if is_dragging:
        mouse_pos = pg.mouse.get_pos()
        for tile in tiles.sprites():
            tile.rect.x += mouse_pos[0] - drag_start[0]
            tile.rect.y += mouse_pos[1] - drag_start[1]

        drag_start = mouse_pos

    level_size = level.get_size()
    scaled_level = pg.transform.scale(
        level, (level_size[0] * zoom, level_size[1] * zoom))
    editor.blit(scaled_level, (0, 0))
    screen.blit(editor, (0, 0))

    pg.display.update()
    clock.tick(60)
