import pygame as pg

from utils import load_image
import config
from .button import Button
from .playable_scene import PlayableScene


class Menu:
    def __init__(self, change_level):
        self.change_level = change_level

        self.start_btn = Button(
            (240, 80), (config.SCREEN_CENTER[0], config.SCREEN_CENTER[1]), 'Start', self.start, font_size=40)
        self.setting_btn = Button(
            (200, 64), (config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 80), 'Settings', self.settings,  font_size=30)
        self.credits_btn = Button(
            (200, 64), (config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 80 + 72), 'Credits', self.credits, font_size=30)

        self.bg = load_image('assets/bg.png', __file__)
        # Set bg width to screen width and then increase height in the same ratio
        self.bg = pg.transform.smoothscale(
            self.bg, (config.SCREEN_WIDTH, self.bg.get_height() * (config.SCREEN_WIDTH / self.bg.get_width())))

    def start(self):
        self.change_level(PlayableScene(
            self.change_level, './scenes/map/1.json'))

    def settings(self):
        self.change_level(Settings(self.change_level))

    def credits(self):
        self.change_level(Credits(self.change_level))

    def update(self, screen):
        screen.blit(self.bg, (0, 0))
        self.start_btn.draw(screen)
        self.setting_btn.draw(screen)
        self.credits_btn.draw(screen)


class Settings:
    def __init__(self, change_level):
        self.change_level = change_level

        self.start_btn = Button(
            (240, 80), (config.SCREEN_CENTER[0], config.SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40)

        self.bg = load_image('assets/bg.png', __file__)
        # Set bg width to screen width and then increase height in the same ratio
        self.bg = pg.transform.smoothscale(
            self.bg, (config.SCREEN_WIDTH, self.bg.get_height() * (config.SCREEN_WIDTH / self.bg.get_width())))

    def menu(self):
        self.change_level(Menu(self.change_level))

    def update(self, screen):
        screen.blit(self.bg, (0, 0))
        self.start_btn.draw(screen)


class Credits:
    def __init__(self, change_level):
        self.change_level = change_level

        self.start_btn = Button(
            (240, 80), (config.SCREEN_CENTER[0], config.SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40)

        self.bg = load_image('assets/bg.png', __file__)
        # Set bg width to screen width and then increase height in the same ratio
        self.bg = pg.transform.smoothscale(
            self.bg, (config.SCREEN_WIDTH, self.bg.get_height() * (config.SCREEN_WIDTH / self.bg.get_width())))

    def menu(self):
        self.change_level(Menu(self.change_level))

    def update(self, screen):
        screen.blit(self.bg, (0, 0))
        self.start_btn.draw(screen)
