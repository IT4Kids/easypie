# coding=utf-8
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import io

import time
from pyqode.qt import QtCore

import gui.gui_core

class QDbgConsole(QtWidgets.QTextEdit):
    """
    A simple QTextEdit, with a few pre-set attributes and a file-like
    interface.
    """
    log_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self, size=None, parent=None):
        super(QDbgConsole, self).__init__(parent)

        self._buffer = io.StringIO()

        if size:
            self.setMinimumSize(*size)
        self.setReadOnly(True)
        self.getting_input = False
        self.input_cursor_pos = None
        self.log_signal.connect(self.write)
        self.error_signal.connect(lambda msg: self.write(msg, text_color=QtGui.QColor(139, 0, 0)))

    def write(self, msg, text_color=QtGui.QColor(0, 0, 0)):
        """Add msg to the console's output, on a new line."""
        self.setTextColor(text_color)
        self.insertPlainText(msg)
        # Autoscroll
        self.moveCursor(QtGui.QTextCursor.End)
        self._buffer.write(msg)

    def get_input(self, prompt=""):
        self.getting_input = True
        self.log_signal.emit(prompt)
        self.moveCursor(QtGui.QTextCursor.End)
        self.setReadOnly(False)
        self.input_cursor_pos = self.textCursor().position()+len(prompt)
        while self.getting_input:
            time.sleep(0.1)
        self.moveCursor(QtGui.QTextCursor.End)
        ret = self.toPlainText()[self.input_cursor_pos:].strip()
        return ret


    def keyPressEvent(self, event):
        if self.getting_input:
            if event.key() == QtCore.Qt.Key_Return:
                self.setReadOnly(True)
                self.write("\n")
                self.getting_input = False
                return

            if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
                if self.textCursor().position() <= self.input_cursor_pos:
                    return
            super().keyPressEvent(event)
        self.moveCursor(QtGui.QTextCursor.End)


    def __getattr__(self, attr):
        """
        Fall back to the buffer object if an attribute can't be found.
        """
        return getattr(self._buffer, attr)
