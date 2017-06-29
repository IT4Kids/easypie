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
        self.input_buffer = ""
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
        self.setReadOnly(False)
        self.log_signal.emit(prompt)
        self.input_cursor_pos = self.textCursor().position()
        while self.getting_input:
            time.sleep(0.1)
        self.setReadOnly(True)
        self.getting_input = False
        ret = self.input_buffer
        self.input_buffer = ""
        return ret


    def keyPressEvent(self, event):
        if self.getting_input:
            self.moveCursor(QtGui.QTextCursor.End)
            self.input_buffer += event.text()
            if event.key() == QtCore.Qt.Key_Return:
                self.getting_input = False
        else:
            self.moveCursor(QtGui.QTextCursor.End)
        super().keyPressEvent(event)


    def __getattr__(self, attr):
        """
        Fall back to the buffer object if an attribute can't be found.
        """
        return getattr(self._buffer, attr)
