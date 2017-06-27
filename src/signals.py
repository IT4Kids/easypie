"""
Contains all signals as a central point between GUI and Controller.
"""

import PyQt5.QtCore as QtCore


class Signals(QtCore.QObject):
    game_stop_signal = QtCore.pyqtSignal()  # args:
    game_start_signal = QtCore.pyqtSignal(tuple)  # args: code
    save_as_signal = QtCore.pyqtSignal()
    new_signal = QtCore.pyqtSignal()
    save_signal = QtCore.pyqtSignal()
    close_signal = QtCore.pyqtSignal()


all = Signals()
