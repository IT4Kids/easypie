# coding=utf-8
__name__ = "pygame"#For error messages

import pygame
import PyQt5.QtCore as Core
def update_keys():
    for (method, keycode, modifiers) in key_queue:
        cbs = key_callbacks[easypie.core.constants.KEYDOWN].get(keycode, {}).get(modifiers, [])
        for cb in cbs:
            cb()
    key_queue = []

    for keycode in pressed_keys:
        cbs = key_callbacks[easypie.core.constants.KEYPRESSED].get(keycode, {}).get(modifiers, [])
        for cb in cbs:
            cb()

font.Font(None,36) #to fix a bug with lazy loading of pygame

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