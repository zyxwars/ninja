import pygame as pg

from utils import load_image

from .button import Button
from .playable_scene import PlayableScene
import game


class Base:
    def __init__(self, change_level):
        self.change_level = change_level

        self.elements = []

        self.bg = load_image('assets/bg.png', __file__)
        # Set bg width to screen width and then increase height in the same ratio
        self.bg = pg.transform.smoothscale(
            self.bg, (game.SCREEN_WIDTH, self.bg.get_height() * (game.SCREEN_WIDTH / self.bg.get_width())))

    def update(self, screen):
        screen.blit(self.bg, (0, 0))

        for element in self.elements:
            element.draw(screen)


class Menu(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.SCREEN_CENTER[0], game.SCREEN_CENTER[1]), 'Start', self.start, font_size=40))
        self.elements.append(Button(
            (200, 64), (game.SCREEN_CENTER[0], game.SCREEN_CENTER[1] + 80), 'Settings', self.settings,  font_size=30))
        self.elements.append(Button(
            (200, 64), (game.SCREEN_CENTER[0], game.SCREEN_CENTER[1] + 80 + 72), 'Credits', self.credits, font_size=30))

    def start(self):
        self.change_level(PlayableScene(
            self.change_level, game.LEVEL_MAP[1]))

    def settings(self):
        self.change_level(Settings(self.change_level))

    def credits(self):
        self.change_level(Credits(self.change_level))


class Settings(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.SCREEN_CENTER[0], game.SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40))

    def menu(self):
        self.change_level(Menu(self.change_level))


class Credits(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.SCREEN_CENTER[0], game.SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40))

    def menu(self):
        self.change_level(Menu(self.change_level))
