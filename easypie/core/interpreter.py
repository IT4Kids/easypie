# coding=utf-8
import io
import threading
import traceback

import pygame
import sys

import easypie.signals
import easypie.gui.gui_core
from easypie.core import constants


environment = None
def _user_print(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    easypie.gui.gui_core.main_window.centralWidget().stage.console.log_signal.emit(string)

def reset_env():
    """
    Inits or reinits all non-constants.
    :return:
    :rtype:
    """
    global environment, key_callbacks, key_queue, pressed_keys
    environment = {}
    environment['print'] = _user_print
    environment['bg_image'] = None
    screen = pygame.Surface(constants.SCREEN_SIZE)
    key_callbacks = {
        constants.KEYDOWN: {},  # for oneShot keys
        constants.KEYPRESSED: {}  # for pressed keys,
    }
    key_queue = []
    pressed_keys = []

def _user_err(*args, sep=' ', end='\n'):
    string = sep.join([str(arg) for arg in args]) + end
    easypie.gui.gui_core.get_window().centralWidget().stage.console.error_signal.emit(string)

def print_last_exception_to_user():
    file = io.StringIO()
    t, v, tb = sys.exc_info()
    traceback.print_exception(t, v, tb.tb_next, file=file)
    file.seek(0)
    easypie.gui.gui_core.get_window().centralWidget().stage.console.error_signal.emit(file.read())

def interpret(code):
    global environment
    reset_env()
    _user_print("Starting program.\n")
    try:
        exec(code, environment)  # Copying globals to run in current namespace but don't change anything.
    except Exception:
        print_last_exception_to_user()
    finally:
        _user_print("Execution stopped.")
        easypie.signals.all.game_stop_signal.emit()
