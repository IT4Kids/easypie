# coding=utf-8
from pyqode.python.modes import PEP8CheckerMode, CalltipsMode
from pyqode.python.panels import QuickDocPanel
from pyqode.core.modes import CodeCompletionMode
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode.python.widgets import PyCodeEdit


class MyCodeEdit(PyCodeEdit):
    # https://pythonhosted.org/pyqode.python/examples.html
    def __init__(self):
        super().__init__(color_scheme='monokai', autostart_backend=False)
        self.modes.remove(PEP8CheckerMode)
        self.modes.remove(CodeCompletionMode)
        self.modes.remove(CalltipsMode)
        self.panels.remove(QuickDocPanel)
        self.save_on_focus_out = True

class Editor(SplittableCodeEditTabWidget):

    def __init__(self):
        super().__init__()

    def open_file(self,file_path):
        edit = MyCodeEdit()
        edit.file.open(file_path)
        edit.save_on_focus_out = True
        self.add_tab(edit,file_path.split("/")[-1])
