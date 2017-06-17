# coding=utf-8
import threading

import pygame
import sys

import commons
import easypie.signals
import easypie.core.interpreter
import easypie.gui.gui_core as gui

interpreter_thread = None


class InterpreterThread(threading.Thread):
    def __init__(self, code):
        super().__init__()
        self.code_string = code
        self.stop_flag = threading.Event()
        self.setDaemon(True)

    def stop(self):
        self.stop_flag.set()

    def run(self):
        easypie.core.interpreter.interpret(self.code_string)

def run_code(code):
    global interpreter_thread
    if interpreter_thread:
        interpreter_thread.stop()#todo async raise?
        interpreter_thread.join()
    interpreter_thread = InterpreterThread(code)
    interpreter_thread.start()

easypie.signals.all.game_start_signal.connect(run_code)

if __name__ == '__main__':
    pygame.init()
    gui.init(commons.screen)
    ret = gui.app.exec_()
    pygame.quit()
    sys.exit(ret)
