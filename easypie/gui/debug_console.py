# coding=utf-8
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import io
from pyqode.qt import QtCore

from easypie import signals


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
        self.log_signal.connect(self.write)
        self.error_signal.connect(lambda msg: self.write(msg, text_color=QtGui.QColor(139, 0, 0)))

    def write(self, msg, text_color=QtGui.QColor(0, 0, 0)):
        """Add msg to the console's output, on a new line."""
        self.setTextColor(text_color)
        self.insertPlainText(msg.rstrip("\n") + "\n")
        # Autoscroll
        self.moveCursor(QtGui.QTextCursor.End)
        self._buffer.write(msg)



    def __getattr__(self, attr):
        """
        Fall back to the buffer object if an attribute can't be found.
        """
        return getattr(self._buffer, attr)
