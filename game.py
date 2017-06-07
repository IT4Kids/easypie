# coding=utf-8
import io

from pygame import *  # Import pygame fields into our namespace.
from easypie.constants import *

import threading
import traceback
import time
import sys

from easypie import abstract
from easypie import constants
import gui.core

screen = None
GameElement = abstract.GameElement


class GameThread(threading.Thread):
    def __init__(self, loop=None):
        super().__init__()
        self.user_loop = loop
        self.stop_flag_set = False
        self.pause_flag_set = False

    def set_loop(self, loop):
        self.user_loop = loop

    @property
    def paused(self):
        return self.pause_flag_set

    @paused.setter
    def paused(self, value):
        self.pause_flag_set = value

    def run(self):
        global key_queue, key_callbacks, pressed_keys
        clock = pygame.time.Clock()
        key_queue = []
        while not self.stop_flag_set:

            while self.pause_flag_set:
                time.sleep(0.1)

            clock.tick(constants.MAX_FPS)  # Enforce fpsmax
            try:
                for (method, key_string, modifiers) in key_queue:
                    key_string = key_string.lower()
                    modifiers = int(modifiers)
                    cbs = key_callbacks[KEYDOWN].get(key_string, {}).get(modifiers, [])
                    for cb in cbs:
                        cb()
                key_queue = []

                for key_string in pressed_keys:
                    cbs = key_callbacks[KEYPRESSED].get(key_string.lower(), {}).get(0, [])
                    for cb in cbs:
                        cb()

                gui.core.loop()

                self.user_loop()
            except Exception as e:
                print_exception_to_console()
                self.stop()

    def stop(self):
        self.stop_flag_set = True


game_thread = GameThread()


def init():
    global screen
    pygame.init()
    screen = pygame.Surface(constants.SCREEN_SIZE)


#todo reset_environment
key_callbacks = {
    constants.KEYDOWN: {},  # for oneShot keys
    constants.KEYPRESSED: {}  # for pressed keys,
}
key_queue = []
pressed_keys = []


def on_key(key_constant, cb, modifiers=None, method=constants.KEYDOWN):

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
    global game_thread
    if game_thread:
        game_thread.stop()
    game_thread = GameThread()
    game_thread.set_loop(loop)
    game_thread.start()


def print_exception_to_console():
    file = io.StringIO()
    t, v, tb = sys.exc_info()
    traceback.print_exception(t, v, tb.tb_next, file=file)
    file.seek(0)
    gui.core.main_window.centralWidget().stage.console.error_signal.emit(file.read())


def execute(code):
    try:
        exec(code, globals().copy())  # Copying globals to run in current namespace but don't change anything.
    except Exception as e:
        game_thread.stop()
        print_exception_to_console()
