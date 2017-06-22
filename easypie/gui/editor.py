# coding=utf-8
from pyqode.python.modes import PEP8CheckerMode
from pyqode.python.widgets import PyCodeEdit


class Editor(PyCodeEdit):
    # https://pythonhosted.org/pyqode.python/examples.html
    def __init__(self):
        super().__init__(color_scheme='monokai')
        self.modes.remove(PEP8CheckerMode)

