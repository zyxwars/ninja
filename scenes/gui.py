import pygame as pg

import config
from utils.load_image import load_image


class Gui:
    def __init__(self):
        self.life_essence = load_image('assets/hp.png', __file__)
        self.flag = load_image('assets/flag.png', __file__)
        self.font = pg.font.Font(None, 24)

    def draw_equipped_weapon(self, weapon, surface):
        surface.blit(weapon, (0, 0))

    def draw_life_essence(self, hp, surface):
        bar_height = 6
        bg_bar = pg.Surface((100, bar_height))
        regen_bar = pg.Surface((min(hp + 25, 100), bar_height))
        regen_bar.fill('gray')
        hp_bar = pg.Surface((hp, bar_height))
        hp_bar.fill('white')

        surface.blit(bg_bar, bg_bar.get_rect(
            midleft=(config.SCREEN_WIDTH - 132, 20)))

        surface.blit(regen_bar, regen_bar.get_rect(
            midleft=(config.SCREEN_WIDTH - 132 + (100 - min(hp + 25, 100)), 20)))

        surface.blit(hp_bar, hp_bar.get_rect(
            midleft=(config.SCREEN_WIDTH - 132 + (100 - hp), 20)))

        surface.blit(self.life_essence, self.life_essence.get_rect(
            center=((config.SCREEN_WIDTH - 16, 20))))

    def draw_flags_collected(self, flags_collected, surface):
        text = self.font.render(
            f'Flags collected: {flags_collected}', True, 'black')
        rect = text.get_rect(
            center=(config.SCREEN_WIDTH - 96, 64))

        surface.blit(text, rect)
        surface.blit(self.flag, self.flag.get_rect(
            center=((config.SCREEN_WIDTH - 16, 64))))
