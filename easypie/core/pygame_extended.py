# coding=utf-8
__name__ = "pygame"

from pygame import *
import pygame
import PyQt5.QtCore as Core

from easypie.core.abstract import GameElement
from easypie.core.game_bindings import on_key, screen, run, set_background

pygame.init()
font.Font("res/freesansbold.ttf",36)

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