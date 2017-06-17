# coding=utf-8
import io
import threading
import traceback
import sys

import pygame
import time

import easypie
import easypie.core.constants as constants
import easypie.gui.gui_core
import easypie.signals

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
        self.is_running = True
        global key_queue, key_callbacks, pressed_keys, screen, background_image
        clock = pygame.time.Clock()
        key_queue = []
        while not self.stop_flag_set:
            while self.pause_flag_set:
                time.sleep(0.1)

            clock.tick(easypie.core.constants.MAX_FPS)  # Enforce fpsmax
            try:
                for (method, keycode, modifiers) in key_queue:
                    cbs = key_callbacks[easypie.core.constants.KEYDOWN].get(keycode, {}).get(modifiers, [])
                    for cb in cbs:
                        cb()
                key_queue = []

                for keycode in pressed_keys:
                    cbs = key_callbacks[easypie.core.constants.KEYPRESSED].get(keycode, {}).get(modifiers, [])
                    for cb in cbs:
                        cb()

                screen.fill((0, 0, 0))
                if background_image:
                    screen.blit(background_image,(0,0))
                self.user_loop()
                easypie.gui.gui_core.loop()

            except Exception as e:
                _print_exception_to_console()
                easypie.signals.all.game_stop_signal.emit()
                self.stop()
        self.is_running = False

    def stop(self):
        self.stop_flag_set = True

_game_thread = GameThread()

background_image = None
screen = pygame.Surface(constants.SCREEN_SIZE)
key_callbacks = {
    constants.KEYDOWN: {},  # for oneShot keys
    constants.KEYPRESSED: {}  # for pressed keys,
}
key_queue = []
pressed_keys = []

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
    _game_thread = GameThread()
    _game_thread.set_loop(loop)
    _game_thread.start()


def _setup_environment():
    global key_callbacks, key_queue, pressed_keys

    key_callbacks = {
        constants.KEYDOWN: {},  # for oneShot keys
        constants.KEYPRESSED: {}  # for pressed keys,
    }
    key_queue = []
    pressed_keys = []
    user_glob = {}
    user_glob["print"] = _console_print
    return user_glob

def set_background(file_path=None):
    global background_image
    if not file_path.endswith(".bmp"):
        _console_err("Warning: Loading background: You should always use .bmp-formatted images.")
    background_image = pygame.image.load(file_path)
    background_image = pygame.transform.scale(background_image,constants.SCREEN_SIZE)

def _console_print(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    easypie.gui.gui_core.main_window.centralWidget().stage.console.log_signal.emit(string)

def _console_err(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    easypie.gui.gui_core.main_window.centralWidget().stage.console.error_signal.emit(string)

def _print_exception_to_console():
    file = io.StringIO()
    t, v, tb = sys.exc_info()
    traceback.print_exception(t, v, tb.tb_next, file=file)
    file.seek(0)
    easypie.gui.gui_core.main_window.centralWidget().stage.console.error_signal.emit(file.read())


def _execute(code):
    try:
        _console_print("Starting program.\n")
        exec(code, _setup_environment())  # Copying globals to run in current namespace but don't change anything.
    except Exception:
        _print_exception_to_console()
    finally:
        easypie.signals.all.game_stop_signal.emit()

easypie.signals.all.game_start_signal.connect(_execute)
easypie.signals.all.game_stop_signal.connect(_game_thread.stop)
import easypie.core.pygame_extended
sys.modules['pygame'] = sys.modules['easypie.core.pygame_extended']