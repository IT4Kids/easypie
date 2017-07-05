# coding=utf-8
import os

from pygame import *
import pygame
import math
import PyQt5.QtCore as Core

from common import res
from core.game_bindings import on_key, screen, run, set_background

__name__ = "pygame"

pygame.init()

real_font = pygame.font.Font
abs_path = os.path.abspath(res('gui/res/freesansbold.ttf'))


def font_workaround(path, size):
    if path is None:
        path = abs_path
    return real_font(path, size)


pygame.font.Font = font_workaround

font.Font(None, 36)

KMOD_ALT = Core.Qt.AltModifier
KMOD_CTRL = Core.Qt.ControlModifier
KMOD_META = Core.Qt.MetaModifier
KMOD_NONE = Core.Qt.NoModifier
KMOD_SHIFT = Core.Qt.ShiftModifier

KEYDOWN = pygame.KEYDOWN
KEYUP = pygame.KEYUP
KEYPRESSED = 0

WIDTH = 1600
HEIGHT = 900
SCREEN_SIZE = (WIDTH, HEIGHT)


def render_text(surface, string, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text = font.render(string, 1, color)
    surface.blit(text, (x, y))

class GameElement(pygame.sprite.Sprite):

    def __init__(self,*groups):
        super().__init__(groups)
        self.direction = 0
        self._image = pygame.Surface((0,0))
        self._rect = self._image.get_rect()
        self._x = 0
        self._y = 0

    def collides(self, sprite):
        return pygame.sprite.spritecollide(self,pygame.sprite.Group(sprite),False)


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._rect.x = value
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._rect.y = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._rect = value.get_rect()

    @property
    def rect(self):
        return self._rect

    def rotate(self, degree):
        self.direction += degree

    def move(self, steps):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += steps * math.sin(direction_radians)
        self.y -= steps * math.cos(direction_radians)

    def draw(self, surface):
        pygame.sprite.Group(self).draw(surface)
