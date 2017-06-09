"""
Contains all signals as a central point between GUI and Controller.
"""

import PyQt5.QtCore as core

class Signals(core.QObject):
    game_stop_signal = core.pyqtSignal() #args:
    game_start_signal = core.pyqtSignal(str) #args: code
all = Signals()