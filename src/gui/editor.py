# coding=utf-8
import sys

from pyqode.python.modes import PEP8CheckerMode, CalltipsMode
from pyqode.python.panels import QuickDocPanel
from pyqode.core.modes import CodeCompletionMode
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode.python.widgets import PyCodeEdit

import src.signals

class MyCodeEdit(PyCodeEdit):
    # https://pythonhosted.org/pyqode.python/examples.html
    def __init__(self, parent=None):


        super().__init__(parent=parent,color_scheme='monokai', autostart_backend=not getattr(sys,'frozen',False))
        self.modes.remove(PEP8CheckerMode)
        if not self.backend.running:
            self.modes.remove(CodeCompletionMode)
            self.modes.remove(CalltipsMode)
            self.panels.remove(QuickDocPanel)


class Editor(SplittableCodeEditTabWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.register_code_edit(MyCodeEdit)
        src.signals.all.save_as_signal.connect(self.save_current_as)
        src.signals.all.save_signal.connect(self.save_current)
        src.signals.all.new_signal.connect(lambda: self.create_new_document(extension=".py"))

    def save_current(self):
        if self.current_widget():
            if not self.current_widget().file.path:
                self.save_current_as()
            else:
                super().save_current()

    def get_code(self):
        if self.current_widget():
            return self.current_widget().toPlainText()
        return ""