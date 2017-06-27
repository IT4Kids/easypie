# coding=utf-8
from pygame import *
import pygame
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
