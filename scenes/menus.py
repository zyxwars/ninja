import pygame as pg

from utils import load_image

from .button import Button
from .playable_scene import PlayableScene
import game


class Base:
    def __init__(self):
        self.elements = []

        self.bg = load_image('assets/bg.png', __file__)
        # Set bg width to screen width and then increase height in the same ratio
        self.bg = pg.transform.smoothscale(
            self.bg, (game.RENDER_SCREEN_WIDTH, self.bg.get_height() * (game.RENDER_SCREEN_WIDTH / self.bg.get_width())))

    def update(self, screen):
        screen.blit(self.bg, (0, 0))

        for element in self.elements:
            element.draw(screen)


class Menu(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.RENDER_SCREEN_CENTER[0], game.RENDER_SCREEN_CENTER[1]), 'Start', self.start, font_size=40))
        self.elements.append(Button(
            (200, 64), (game.RENDER_SCREEN_CENTER[0], game.RENDER_SCREEN_CENTER[1] + 80), 'Settings', self.settings,  font_size=30))
        self.elements.append(Button(
            (200, 64), (game.RENDER_SCREEN_CENTER[0], game.RENDER_SCREEN_CENTER[1] + 80 + 72), 'Credits', self.credits, font_size=30))

    def start(self):
        game.loop.change_scene(PlayableScene(game.LEVEL_MAP[0]))

    def settings(self):
        game.loop.change_scene(Settings())

    def credits(self):
        game.loop.change_scene(Credits())


class Settings(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.RENDER_SCREEN_CENTER[0], game.RENDER_SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40))

    def menu(self):
        game.loop.change_scene(Menu())


class Credits(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements.append(Button(
            (240, 80), (game.RENDER_SCREEN_CENTER[0], game.RENDER_SCREEN_CENTER[1]), 'Menu', self.menu,  font_size=40))

    def menu(self):
        game.loop.change_scene(Menu())
