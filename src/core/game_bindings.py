# coding=utf-8
import io
import threading
import traceback
import sys
import os

import pygame
import time

import core.constants as constants
import gui.gui_core
import signals


class GameThread(threading.Thread):
    def __init__(self, loop=None):
        super().__init__()
        self.user_loop = loop
        self.stop_flag_set = False
        self.pause_flag_set = False
        self.is_running = False

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

            clock.tick(core.constants.MAX_FPS)  # Enforce fpsmax
            try:
                for (method, keycode, modifiers) in key_queue:
                    cbs = key_callbacks[core.constants.KEYDOWN].get(keycode, {}).get(modifiers, [])
                    for cb in cbs:
                        cb()
                key_queue = []

                for keycode in pressed_keys:
                    cbs = key_callbacks[core.constants.KEYPRESSED].get(keycode, {}).get(modifiers, [])
                    for cb in cbs:
                        cb()

                screen.fill((0, 0, 0))
                if background_image:
                    screen.blit(background_image, (0, 0))
                self.user_loop()
                gui.gui_core.loop()

            except Exception as e:
                traceback.print_exc()
                print("Exception in GameThread", e)
                _print_exception_to_console()
                signals.all.game_stop_signal.emit()
                self.stop()

        self.is_running = False

    def stop(self):
        self.stop_flag_set = True


game_thread = GameThread()

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
    global game_thread
    if game_thread:
        game_thread.stop()
    game_thread = GameThread()
    game_thread.set_loop(loop)
    game_thread.start()


def _setup_environment(file_path=None):
    if file_path:
        os.chdir(os.path.dirname(file_path))

    global key_callbacks, key_queue, pressed_keys, background_image

    background_image = None

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
    if file_path:
        if not file_path.endswith(".bmp"):
            _console_err("Warning: Loading background: You should always use .bmp-formatted images.")
        background_image = pygame.image.load(file_path)
        background_image = pygame.transform.scale(background_image, constants.SCREEN_SIZE)
    else:
        background_image = None


def _console_print(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    gui.gui_core.main_window.centralWidget().stage.console.log_signal.emit(string)


def _console_err(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    gui.gui_core.main_window.centralWidget().stage.console.error_signal.emit(string)


def _console_clear():
    gui.gui_core.main_window.centralWidget().stage.console.clear()  # Change this to a signal later one, fix bug
    # with signal in incorrect order


def _print_exception_to_console():
    file = io.StringIO()
    t, v, tb = sys.exc_info()
    traceback.print_exception(t, v, tb.tb_next, file=file)
    file.seek(0)
    gui.gui_core.main_window.centralWidget().stage.console.error_signal.emit(file.read())


def _execute(code):
    old_path = os.getcwd()
    if game_thread.is_running:
        game_thread.stop()
        game_thread.join()
    try:
        _console_clear()
        _console_print(">>> Starting program.")
        sys.path.append(os.path.dirname(code[1]))
        exec(code[0],
             _setup_environment(code[1]))  # Copying globals to run in current namespace but don't change anything.
    except Exception:
        _print_exception_to_console()
    finally:
        sys.path.remove(os.path.dirname(code[1]))
        os.chdir(old_path)
        signals.all.game_stop_signal.emit()


signals.all.game_start_signal.connect(_execute)
signals.all.game_stop_signal.connect(game_thread.stop)
import core.pygame_extended #Has sideeffects

sys.modules['pygame'] = sys.modules['core.pygame_extended']
