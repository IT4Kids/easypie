"""
Contains all signals as a central point between GUI and Controller.
"""

import PyQt5.QtCore as core

class Signals(core.QObject):
    game_stop_signal = core.pyqtSignal() #args:
    game_start_signal = core.pyqtSignal(str) #args: code
    save_as_signal = core.pyqtSignal()
    new_signal = core.pyqtSignal()
    save_signal = core.pyqtSignal()
    close_signal = core.pyqtSignal()

all = Signals()