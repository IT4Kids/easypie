# coding=utf-8
from PyQt5 import QtGui
from PyQt5.QtGui import QColor

from pyqode.core.api import TextDecoration
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit
from pyqode.python.modes import PEP8CheckerMode


class Editor(PyCodeEdit):
    # https://pythonhosted.org/pyqode.python/examples.html
    def __init__(self):
        super().__init__(server_script=server.__file__, color_scheme='monokai')
        self.modes.remove(PEP8CheckerMode)

