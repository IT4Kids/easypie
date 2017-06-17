# coding=utf-8
import threading
import time

import pygame

import easypie
import easypie.core.constants as constants
import easypie.core.interpreter
import easypie.signals

def on_key(key_constant, cb, modifiers=None, method=constants.KEYDOWN):
    """
    Create a key-callback for a given pygame key.

    :param key_constant: A key-code (e.g. pygame.K_a) for "a"
    :type key_constant: int
    :param cb: The callback function
    :type cb: method
    :param modifiers: A list of modifiers.
    :type modifiers: List[int]
    :param method: pygame.KEYDOWN or pygame.KEYPRESSED, decides wether function is called multiple times on press.
    :type method: int

    """

    # Create modifiers mask
    if modifiers is None:
        modifiers = []
    mod_mask = 0
    for mod in modifiers:
        mod_mask |= int(mod)
    if method not in [constants.KEYDOWN, constants.KEYPRESSED]:
        raise RuntimeError("on_key requires KEYDOWN or KEYPRESSED.")

    cb_dict = key_callbacks[method].get(key_constant, {})
    cb_mod_list = cb_dict.get(mod_mask, [])
    cb_mod_list.append(cb)
    cb_dict[mod_mask] = cb_mod_list
    key_callbacks[method][key_constant] = cb_dict
    print("Keycallback: ", method, key_constant, mod_mask)

def run(loop):
    global _game_thread
    if _game_thread:
        _game_thread.stop()
    _game_thread = UserThread()
    _game_thread.set_loop(loop)
    _game_thread.start()


def set_background(file_path=None):
    global background_image
    if not file_path.endswith(".bmp"):
        user_err("Warning: Loading background: You should always use .bmp-formatted images.")
    background_image = pygame.image.load(file_path)
    background_image = pygame.transform.scale(background_image,constants.SCREEN_SIZE)



