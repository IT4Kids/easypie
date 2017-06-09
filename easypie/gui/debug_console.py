# coding=utf-8
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import io
from pyqode.qt import QtCore


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

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(240,240,255))
        self.setPalette(palette)

    def write(self, msg, text_color=QtGui.QColor(0, 0, 0)):
        """Add msg to the console's output, on a new line."""
        self.setTextColor(text_color)
        self.insertPlainText(msg.rstrip("\n") + "\n")
        # Autoscroll
        self.moveCursor(QtGui.QTextCursor.End)
        self._buffer.write(msg)

    def clear(self):
        self.setText("")

    def __getattr__(self, attr):
        """
        Fall back to the buffer object if an attribute can't be found.
        """
        return getattr(self._buffer, attr)
